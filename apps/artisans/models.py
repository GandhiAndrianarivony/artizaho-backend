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
