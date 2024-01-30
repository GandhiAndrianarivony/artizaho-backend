"""Module for creating individuals contacts"""

from django.db import models

from apps.users.models import User


class Contact(models.Model):
    email = models.EmailField(db_index=True, max_length=255)
    phone_number = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
