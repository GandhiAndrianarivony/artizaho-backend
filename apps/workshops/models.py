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

    def get_workshop_info(self):
        return self.informations.all().order_by("-created_at").first()
    
    def __str__(self) -> str:
        return self.title


class WorkshopInfo(models.Model):
    workshop = models.ForeignKey(
        Workshop, related_name="informations", on_delete=models.SET_NULL, null=True
    )
    max_participants = models.PositiveIntegerField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(
        max_length=5,
        choices=CurrencyType.choices(),
        db_default=CurrencyType.DOLLARS.value,
    )
    created_at = models.DateTimeField(auto_now_add=True)


class CustomWorkshop(models.Model):
    user = models.ForeignKey(
        User, related_name="custom_workshops", on_delete=models.SET_NULL, null=True
    )
    workshop = models.ForeignKey(
        Workshop, related_name="customizes", on_delete=models.SET_NULL, null=True
    )
    date = models.DateField()
    time = models.TimeField()
    number_of_participants = models.PositiveIntegerField()
    location = models.TextField()
    status = models.CharField(
        max_length=100,
        choices=CustomWorkshopStatus.choices(),
        default=CustomWorkshopStatus.NEW.value,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_enterprise = models.BooleanField(default=False, null=True)


class WorkshopBookable(models.Model):
    workshop_info = models.ForeignKey(
        WorkshopInfo, related_name="bookables", on_delete=models.CASCADE, null=True
    )
    artisan = models.ForeignKey(
        Artisan, related_name="bookable_workshops", on_delete=models.SET_NULL, null=True
    )
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    time = models.TimeField(null=True)
    duration = models.PositiveIntegerField(verbose_name="Duration in seconds")
    available_places = models.IntegerField()
    location = models.TextField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True, auto_now_add=True)


class WorkshopReservation(models.Model):
    workshop_bookable = models.ForeignKey(
        WorkshopBookable, related_name="workshop_booked", on_delete=models.SET_NULL, null=True
    )
    user = models.ForeignKey(
        User, related_name="reservations", on_delete=models.SET_NULL, null=True
    )
    payment_status = models.CharField(max_length=125, choices=PaymentStatus.choices())
    number_of_participants = models.PositiveIntegerField()
    custom_workshop = models.ForeignKey(
        CustomWorkshop, related_name="custom_workshop_booked", on_delete=models.SET_NULL, null=True
    )
    artisan = models.ForeignKey(
        Artisan, related_name="custom_workshop", null=True, on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
