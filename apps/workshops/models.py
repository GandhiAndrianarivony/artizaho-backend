"""Workshop related modules"""

from django.db import models

from apps.artisans.models import ExpertiseChoice, Artisan
from apps.users.models import User
from apps.payments.choices import PaymentStatus

from .choices import CurrencyType, CustomWorkshopStatus


class Workshop(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255, choices=ExpertiseChoice.choices())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class WorkshopInfo(models.Model):
    workshop = models.ForeignKey(
        Workshop, related_name="informations", on_delete=models.SET_NULL, null=True
    )
    artisan = models.ForeignKey(
        Artisan, related_name="artisans", on_delete=models.SET_NULL, null=True
    )
    max_participant = models.PositiveIntegerField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=5, choices=CurrencyType.choices())
    created_at = models.DateTimeField(auto_now_add=True)


class CustomWorkshop(models.Model):
    user = models.ForeignKey(
        User, related_name="custom_workshops", on_delete=models.SET_NULL, null=True
    )
    workshop_info = models.ForeignKey(
        WorkshopInfo, related_name="customs", on_delete=models.SET_NULL, null=True
    )
    date = models.DateField()
    time = models.TimeField()
    number_of_participants = models.PositiveIntegerField()
    location = models.TextField()
    status = models.CharField(max_length=100, choices=CustomWorkshopStatus.choices())


class WorkshopBookable(models.Model):
    workshop_info = models.ForeignKey(
        WorkshopInfo, related_name="bookables", on_delete=models.CASCADE
    )
    date = models.DateField()
    time = models.TimeField()
    available_places = models.IntegerField()
    location = models.TextField()
    duration = models.PositiveIntegerField(verbose_name="Duration in seconds")
    is_available = models.BooleanField(default=True)


class WorkshopReservation(models.Model):
    workshop_bookable = models.ForeignKey(
        WorkshopBookable, related_name="booked", on_delete=models.SET_NULL, null=True
    )
    user = models.ForeignKey(
        User, related_name="reservations", on_delete=models.SET_NULL, null=True
    )
    payment_status = models.CharField(max_length=125, choices=PaymentStatus.choices())
    number_of_participants = models.PositiveIntegerField()
    custom_workshop = models.ForeignKey(
        CustomWorkshop, related_name="booked", on_delete=models.SET_NULL, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
