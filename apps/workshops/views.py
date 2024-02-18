"""Workshop view module"""

from typing import Dict


from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action

from django.db import transaction
from django.shortcuts import get_object_or_404
import django_filters

from apps.artisans.models import Artisan
from apps.artisans.exceptions import ArtisanNotFound
from apps.workshops.models import WorkshopBookable

from api import mixins as api_mixins
from api.permissions import AllowListPermission

from .serializers import (
    WorkshopSerializer,
    WorkshopInfoSerializer,
    WorkshopBookableSerializer,
)
from .models import Workshop, WorkshopInfo
from .exceptions import WorkshopNotFound
from .helpers import remove_dict_key, update_dict
from .filters import WorkshopBookableFilter, WorkshopBookableOrdiring


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
        artisan = workshop_infos.pop("artisan")
        try:
            artisan = Artisan.objects.get(pk=artisan["id"])
        except Artisan.DoesNotExist:
            raise ArtisanNotFound(f"Artisan of pk: {artisan['id']} Not found")

        WorkshopInfo.objects.create(
            workshop=workshop, artisan=artisan, **workshop_infos
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
            pk (int): primary key of an workshop

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
        data["available_places"] = workshop_info.max_participants

        serializer = WorkshopBookableSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        workshop_bookable = WorkshopBookable.objects.create(
            workshop_info=workshop_info, **data
        )
        return Response(
            WorkshopBookableSerializer(workshop_bookable).data,
            status=status.HTTP_201_CREATED,
        )
