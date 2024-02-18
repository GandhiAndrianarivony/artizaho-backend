from django.db import transaction

from rest_framework import serializers

from apps.images.serializers import ImageSerializer

from .models import Artisan, ArtisanAvailability, ArtisanTimeAvailability


class ArtisanSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    availabilities = serializers.SerializerMethodField()

    class Meta:
        model = Artisan
        fields = "__all__"

    def get_images(self, instance: Artisan):
        images = instance.images.all()
        return ImageSerializer(images, many=True).data

    def get_availabilities(self, instance: Artisan):
        availabilities = instance.availabilities.all()
        return ArtisanAvailabilitySerializer(availabilities, many=True).data


class ArtisanTimeAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtisanTimeAvailability
        fields = ["id", "start_time", "end_time"]


class ArtisanAvailabilitySerializer(serializers.ModelSerializer):
    hours = ArtisanTimeAvailabilitySerializer(many=True, required=True)

    class Meta:
        model = ArtisanAvailability
        fields = "__all__"

    def create(self, validated_data):
        hours = validated_data.pop("hours")
        with transaction.atomic():
            availability = ArtisanAvailability.objects.create(
                artisan=self.context.get("artisan"), **validated_data
            )

            hrs = []
            for hour in hours:
                hrs.append(ArtisanTimeAvailability(availability=availability, **hour))
            ArtisanTimeAvailability.objects.bulk_create(hrs)

            return availability

        return ArtisanAvailability.objects.none()
