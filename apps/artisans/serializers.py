from django.db import transaction

from rest_framework import serializers

from apps.images.serializers import ImageSerializer

from .models import Artisan, ArtisanAvailability, ArtisanTimeAvailability


class ArtisanSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    availabilities = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()

    class Meta:
        model = Artisan
        fields = "__all__"

    def get_images(self, instance: Artisan):
        images = instance.images.all()
        return ImageSerializer(images, many=True).data

    def get_availabilities(self, instance: Artisan):
        availabilities = instance.availabilities.all()
        return ArtisanAvailabilitySerializer(availabilities, many=True).data

    def get_stats(self, instance: Artisan):
        total_client = 0
        workshops = set()

        artisan_bookable_workshops = instance.bookable_workshops.all().prefetch_related(
            "workshop_booked", "workshop_info"
        )
        artisan_custom_workshops = instance.custom_workshop.all()

        # Update total_client owned by artisan
        for a_bw in artisan_bookable_workshops:
            booked_workshops = a_bw.workshop_booked.all()
            total_client += self._get_total_client(booked_workshops)
            if booked_workshops.count():
                workshops.add(a_bw.workshop_info.workshop.title)
        total_client += artisan_custom_workshops.count()

        return {"total_client": total_client, "workshops": list(workshops)}

    @staticmethod
    def _get_total_client(reservations):
        total_client = 0
        if reservations.count():
            for reservation in reservations:
                total_client += reservation.number_of_participants
        return total_client


class ArtisanTimeAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtisanTimeAvailability
        fields = ["id", "start_time", "end_time"]


class ArtisanAvailabilitySerializer(serializers.ModelSerializer):
    hours = ArtisanTimeAvailabilitySerializer(many=True, required=True)

    class Meta:
        model = ArtisanAvailability
        fields = "__all__"

    @transaction.atomic
    def create(self, validated_data):
        hours = validated_data.pop("hours")
        availability = ArtisanAvailability.objects.create(
            artisan=self.context.get("artisan"), **validated_data
        )

        hrs = []
        for hour in hours:
            hrs.append(ArtisanTimeAvailability(availability=availability, **hour))
        ArtisanTimeAvailability.objects.bulk_create(hrs)

        return availability
