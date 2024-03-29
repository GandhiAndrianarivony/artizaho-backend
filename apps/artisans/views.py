from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
)

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.artisans.models import Artisan
from apps.artisans.serializers import ArtisanSerializer
from api import mixins as api_mixins

from .serializers import ArtisanAvailabilitySerializer


@extend_schema_view(
    list=extend_schema(
        summary="Return a paginated list of artisan",
        responses={"200": ArtisanSerializer(many=True)},
    )
)
class ArtisanViewset(
    api_mixins.SerializerContextMixin, api_mixins.ImageMixin, viewsets.ModelViewSet
):
    queryset = Artisan.objects.all()
    serializer_class = ArtisanSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(methods=["post"], detail=True, url_path="availability")
    def set_availability(self, request, pk=None, *args, **kwargs):
        artisan = self.get_object()

        serializer = ArtisanAvailabilitySerializer(
            data=request.data, context=self.get_serializer_context(artisan=artisan)
        )
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        return Response(serializer.data)

    # @action(methods=["get"], detail=True, url_path="stats")
    # def get_artisan_stats(self, request, pk=None, *args, **kwargs):
    #     """Generate artisan statistics"""
    #     # Get artisan
    #     artisan = self.get_object()

    #     # Get Artisan Bookable workshop such that they are booked
    #     artisan_bookable_workshops = artisan.bookable_workshops.all().prefetch_related(
    #         "booked"
    #     )
    #     for a_bw in artisan_bookable_workshops:
    #         reservations = a_bw.booked.all()
    #         if reservations.count():
    #             breakpoint()
    #         print(reservations)

    #     # Get Artisan Custom workshop such that they are booked
    #     breakpoint()
