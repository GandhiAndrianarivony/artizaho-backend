from django.db import models

from .choices import ExpertiseChoice


class Artisan(models.Model):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"

    GENDERS = {MALE: "Male", FEMALE: "Female", OTHER: "Other"}

    GENDER = {}
    name = models.CharField(max_length=255)
    description = models.TextField()
    expertise = models.CharField(max_length=255, choices=ExpertiseChoice.choices())
    gender = models.CharField(max_length=10, choices=GENDERS)


class ArtisanAvailability(models.Model):
    artisan = models.ForeignKey(
        Artisan, related_name="availabilities", on_delete=models.CASCADE, null=True
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True)


class ArtisanTimeAvailability(models.Model):
    availability = models.ForeignKey(
        ArtisanAvailability, related_name="hours", on_delete=models.CASCADE, null=True
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
