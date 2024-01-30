from enum import Enum

from django.db import models


class ExpertiseChoice(str, Enum):
    FLORAL = "FLORAL"

    @classmethod
    def choices(cls):
        return tuple((x.value, x.name) for x in cls)

    def __str__(self) -> str:
        return f"{self.value}"


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
