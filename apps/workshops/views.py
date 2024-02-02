"""Workshop view module"""

from typing import Dict

import deepdiff

from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.artisans.models import Artisan
from apps.artisans.exceptions import ArtisanNotFound

from .serializers import WorkshopSerializer, WorkshopInfoSerializer
from .models import Workshop, WorkshopInfo
from .exceptions import WorkshopNotFound


class WorkshopViewset(viewsets.GenericViewSet):
    serializer_class = WorkshopSerializer
    queryset = Workshop.objects.all()

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
        workshop = serializer.save()

        self.create_workshop_info(workshop_infos, workshop)

        return Response(
            self.get_serializer(workshop).data, status=status.HTTP_201_CREATED
        )

    def create_workshop_info(self, workshop_infos: Dict, workshop: Workshop):
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
            workshop_info = self.update_dict(current=dict(current_workshop_info), new=workshop_info)
            self.remove_dict_key(workshop_info, "id", "created_at", "workshop")

            # Remove artisan
            artisan = workshop_info.pop("artisan")
            WorkshopInfoSerializer(data=workshop_info).is_valid(raise_exception=True)

            # Add Artisan
            workshop_info["artisan"] = artisan
            self.create_workshop_info(workshop_info, workshop)

        return Response(
            self.get_serializer(workshop).data, status=status.HTTP_201_CREATED
        )

    def perform_update(self, workshop, data):
        serializer = self.get_serializer(workshop, data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    @staticmethod
    def remove_dict_key(obj, *keys):
        if keys:
            for key in keys:
                obj.pop(key, None)

    @staticmethod
    def update_dict(current, new):
        return {**current, **new}
