from rest_framework import serializers

from apps.artisans.serializers import ArtisanSerializer
from apps.artisans.models import Artisan
from apps.images.serializers import ImageSerializer

from .models import Workshop, WorkshopInfo, WorkshopBookable


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
    images = ImageSerializer(
        many=True, required=False
    )  # serializers.SerializerMethodField()

    class Meta:
        model = Workshop
        fields = "__all__"

    def get_workshop_info(self, instance: Workshop):
        qs = instance.get_workshop_info()
        return WorkshopInfoSerializer(qs).data
    

class WorkshopBookableSerializer(serializers.ModelSerializer):
    workshop = serializers.SerializerMethodField()
    class Meta:
        model = WorkshopBookable
        fields = '__all__'


    def get_workshop(self, instance: WorkshopBookable):
        workshop = instance.workshop_info.workshop
        return WorkshopSerializer(workshop).data
