from rest_framework import serializers

from apps.artisans.serializers import ArtisanSerializer
from apps.artisans.models import Artisan
from .models import Workshop, WorkshopInfo


class WorkshopInfoSerializer(serializers.ModelSerializer):
    artisan = serializers.SerializerMethodField()

    class Meta:
        model = WorkshopInfo
        fields = "__all__"

    def get_artisan(self, instance: WorkshopInfo):
        artisan = Artisan.objects.get(id=instance.artisan.id)
        return ArtisanSerializer(artisan).data


class WorkshopSerializer(serializers.ModelSerializer):
    workshop_info = serializers.SerializerMethodField()

    class Meta:
        model = Workshop
        fields = "__all__"

    def get_workshop_info(self, instance: Workshop):
        qs = instance.informations.all().order_by("-created_at").first()
        return WorkshopInfoSerializer(qs).data
