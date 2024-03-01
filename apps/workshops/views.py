"""Workshop view module"""

from typing import Dict
import math

from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action

from django.db import transaction
from django.shortcuts import get_object_or_404
import django_filters

from apps.artisans.models import Artisan
from apps.artisans.exceptions import ArtisanNotFound
from apps.workshops.models import WorkshopBookable
from apps.payments.choices import PaymentStatus
from apps.users.models import User
from apps.users.exceptions import UserNotFound

from api import mixins as api_mixins
from api.permissions import AllowListPermission

from .serializers import (
    WorkshopSerializer,
    WorkshopInfoSerializer,
    WorkshopBookableSerializer,
    CustomWorkshopSerializer,
    WorkshopReservationSerializer,
)
from .models import Workshop, WorkshopInfo, CustomWorkshop, WorkshopReservation
from .exceptions import WorkshopNotFound, NoAvailablePlace, StatusTypeError
from .helpers import remove_dict_key, update_dict
from .filters import WorkshopBookableFilter, WorkshopBookableOrdiring
from .choices import CustomWorkshopStatus

from . import helpers, services


class WorkshopViewset(
    api_mixins.FilterMixin, api_mixins.ImageMixin, viewsets.GenericViewSet
):
    serializer_class = WorkshopSerializer
    queryset = Workshop.objects.all()
    permission_classes = [AllowListPermission]

    def filter_queryset(self, queryset):
        filter_backends = [
            django_filters.rest_framework.DjangoFilterBackend,
            filters.OrderingFilter,
        ]
        if self.action == "schedule_workshop":
            # filter_backends.append(WorkshopBookableFilter)
            # TODO: Search
            ...

        for backend in filter_backends:
            queryset = backend().filter_queryset(self.request, queryset, view=self)

        return queryset

    def get_filterset_class(self):
        if self.action == "schedule_workshop":
            return WorkshopBookableFilter

    def get_queryset(self):
        self.filterset_class = self.get_filterset_class()

        if self.action == "schedule_workshop":
            self.ordering_fields = WorkshopBookableOrdiring

            return WorkshopBookable.objects.filter(
                workshop_info__workshop_id=self.kwargs.get("pk")
            )

        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        serialized_data = serializer.data

        page = self.paginate_queryset(serialized_data)
        if page is not None:
            return self.get_paginated_response(serialized_data)

    def create(self, request, *args, **kwargs):
        data = request.data
        workshop_infos = data.pop("workshop_info")

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            workshop = serializer.save()
            self._create_workshop_info(workshop_infos, workshop)

        return Response(
            self.get_serializer(workshop).data, status=status.HTTP_201_CREATED
        )

    def _create_workshop_info(self, workshop_infos: Dict, workshop: Workshop):
        WorkshopInfo.objects.create(
            workshop=workshop,
            **workshop_infos,
        )

    def partial_update(self, request, pk=None, *arges, **kwargs):
        # Gather data
        data = request.data
        workshop_info = data.pop("workshop_info", None)

        # Get workshop instance
        try:
            workshop = self.get_queryset().get(pk=pk)
            # Perform update on Workshop
            self.perform_update(workshop, data)
        except Workshop.DoesNotExist:
            raise WorkshopNotFound(f"Workshop of pk: {pk} Not found")

        if workshop_info:
            # Get related workshop information
            current_workshop_info_obj = (
                workshop.informations.all().order_by("-created_at").first()
            )
            # Serialize Workshop info object
            current_workshop_info = WorkshopInfoSerializer(
                current_workshop_info_obj
            ).data

            # Merge request workshop info and current workshop info
            workshop_info = update_dict(
                current=dict(current_workshop_info), new=workshop_info
            )
            remove_dict_key(workshop_info, "id", "created_at", "workshop")

            # Remove artisan
            artisan = workshop_info.pop("artisan")
            WorkshopInfoSerializer(data=workshop_info).is_valid(raise_exception=True)

            # Add Artisan
            workshop_info["artisan"] = artisan
            self._create_workshop_info(workshop_info, workshop)

        return Response(
            self.get_serializer(workshop).data, status=status.HTTP_201_CREATED
        )

    def perform_update(self, workshop, data):
        serializer = self.get_serializer(workshop, data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response()

    @action(
        methods=["post", "get"],
        detail=True,
        url_path="schedule",
        permission_classes=[AllowListPermission],
    )
    def schedule_workshop(self, request, pk=None, *args, **kwargs):
        """Used for creating and listing scheduled workshop bookable

        Args:
            request (Object): contains request info
            pk (int): primary key of the workshop

        Returns:
            queryset: paginated queryset
        """

        workshop = get_object_or_404(Workshop, pk=pk)
        workshop_info = workshop.get_workshop_info()

        if request.method == "GET":
            page = self.get_page()
            if page is not None:
                data = WorkshopBookableSerializer(page, many=True).data
                return self.get_paginated_response(data)

        data = request.data
        artisan = data.pop("artisan", None)

        try:
            artisan = Artisan.objects.get(pk=artisan["id"])
        except Artisan.DoesNotExist:
            raise ArtisanNotFound(f"Artisan of pk: {artisan['id']} Not found")

        data["available_places"] = workshop_info.max_participants
        serializer = WorkshopBookableSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        workshop_bookable = WorkshopBookable.objects.create(
            workshop_info=workshop_info, artisan=artisan, **data
        )
        return Response(
            WorkshopBookableSerializer(workshop_bookable).data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        methods=["post"],
        detail=True,
        url_path="customize",
        permission_classes=[IsAuthenticated],
    )
    def customize_workshop(self, request, pk=None, *args, **kwargs):
        """Endpoint used to customize workshops and used by Enterprise"""

        user = request.user
        workshop = get_object_or_404(Workshop, pk=pk)
        serializer = CustomWorkshopSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Get instance of custom workshop from serializer
        instance = serializer.instance
        instance.user = user
        instance.workshop = workshop

        if user.account_type in ["Entreprise", "E"]:
            instance.is_enterprise = True

        instance.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=["get", "post"],
        detail=False,
        url_path="custom_workshop",
        permission_classes=[
            IsAdminUser,
        ],
    )
    def get_custom_workshops(self, request, *args, **kwargs):
        """Used to get list of customworkshop and update custom workshop status"""

        if request.method == "GET":
            qs = CustomWorkshop.objects.all()
            serializer = CustomWorkshopSerializer(qs, many=True)
            serialized_data = serializer.data

            page = self.paginate_queryset(serialized_data)
            if page is not None:
                return self.get_paginated_response(serialized_data)
            return Response(serialized_data)

        if request.method == "POST":
            data = request.data
            custom_workshop = get_object_or_404(
                CustomWorkshop, pk=data.get("custom_workshop_id", math.inf)
            )

            user = services.get_object(
                model=User,
                data=data,
                data_attr="user",
                exception=UserNotFound,
                message="User not found",
                model_field="id",
            )

            artisan = services.get_object(
                model=Artisan,
                data=data,
                data_attr="artisan",
                exception=ArtisanNotFound,
                message="Artisan not found",
                model_field="id",
            )

            try:
                cw_status = CustomWorkshopStatus.to_dict()[data.get("status")]
            except:
                raise StatusTypeError(f"Wrong status code: {data.get('status', '')}")

            services.update_django_model(custom_workshop, "status", cw_status)

            if cw_status == CustomWorkshopStatus.VALID.value:
                _ = WorkshopReservation.objects.create(
                    artisan=artisan,
                    custom_workshop=custom_workshop,
                    number_of_participants=custom_workshop.number_of_participants,
                    user=user,
                )

            return Response(
                CustomWorkshopSerializer(custom_workshop).data,
                status=status.HTTP_201_CREATED,
            )

    @action(
        methods=["post"],
        detail=False,
        url_path="scheduled_workshop/(?P<scheduled_workshop_id>\d+)/booking",
        permission_classes=[IsAuthenticated],
    )
    def book_workshop(self, request, scheduled_workshop_id=None, *args, **kwargs):
        data = request.data
        bookable_workshop = get_object_or_404(
            WorkshopBookable, pk=scheduled_workshop_id
        )  # WorkshopBookable.objects.get(id=scheduled_workshop_id)

        # Check available place
        available_place = bookable_workshop.available_places
        request_place = data.get(
            "number_of_participants",
        )

        if not helpers.is_gte(available_place, request_place):
            raise NoAvailablePlace(
                f"No more available place. Request: {request_place}, expected: <= {available_place}"
            )
        reservation = WorkshopReservation.objects.create(
            workshop_bookable=bookable_workshop,
            user=request.user,
            number_of_participants=request_place,
            payment_status=PaymentStatus.NOT_PAID.value,
        )

        services.update_django_model(
            bookable_workshop, "available_places", available_place - request_place
        )

        return Response(
            WorkshopReservationSerializer(reservation).data,
            status=status.HTTP_200_OK,
        )
