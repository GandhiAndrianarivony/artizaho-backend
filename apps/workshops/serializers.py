from rest_framework import serializers

from apps.artisans.serializers import ArtisanSerializer
from apps.artisans.models import Artisan
from apps.images.serializers import ImageSerializer

from .models import (
    Workshop,
    WorkshopInfo,
    WorkshopBookable,
    CustomWorkshop,
    WorkshopReservation,
)


class WorkshopInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkshopInfo
        fields = "__all__"


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
    artisan = serializers.SerializerMethodField()

    class Meta:
        model = WorkshopBookable
        fields = "__all__"

    def get_workshop(self, instance: WorkshopBookable):
        workshop = instance.workshop_info.workshop
        return WorkshopSerializer(workshop).data

    def get_artisan(self, instance: WorkshopBookable):
        artisan = Artisan.objects.get(id=instance.artisan_id)
        return ArtisanSerializer(artisan).data


class CustomWorkshopSerializer(serializers.ModelSerializer):
    workshops = serializers.SerializerMethodField()

    class Meta:
        model = CustomWorkshop
        fields = "__all__"

    def get_workshops(self, instance: CustomWorkshop):
        workshop = Workshop.objects.get(id=instance.workshop_id)
        return WorkshopSerializer(workshop).data


class WorkshopReservationSerializer(serializers.ModelSerializer):
    workshop_bookable = WorkshopBookableSerializer()
    custom_workshop = CustomWorkshopSerializer()

    class Meta:
        model = WorkshopReservation
        fields = [
            "id",
            "user",
            "number_of_participants",
            "workshop_bookable",
            "payment_status",
            "custom_workshop",
            "created_at",
            "artisan",
        ]
