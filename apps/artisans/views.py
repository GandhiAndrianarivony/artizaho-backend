from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiTypes,
    extend_schema_view,
    extend_schema,
)

from rest_framework import viewsets, permissions

from apps.artisans.models import Artisan
from apps.artisans.serializers import ArtisanSerializer
from api import mixins as api_mixins


@extend_schema_view(
    list=extend_schema(
        summary="Return a paginated list of artisan",
        responses={200: ArtisanSerializer(many=True)},
    )
)
class ArtisanViewset(api_mixins.ImageMixin, viewsets.ModelViewSet):
    queryset = Artisan.objects.all()
    serializer_class = ArtisanSerializer
    permission_classes = [permissions.IsAdminUser]
