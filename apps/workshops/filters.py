from rest_framework import filters
import django_filters

from .models import WorkshopBookable
from api.meta import BaseOrderingMetaclass


class WorkshopBookableOrdiring(metaclass=BaseOrderingMetaclass):
    """Class for ordering data

    Examples:
        GET {{base_url}}/api/v1/workshop/1/schedule?ordering=-available_places
    """

    class Meta:
        fields = ["available_places"]


class WorkshopBookableFilter(django_filters.FilterSet):
    """Class for filtering data

    Examples:
        GET {{base_url}}/api/v1/workshop/1/schedule?available_places__gte=4
    """

    class Meta:
        model = WorkshopBookable
        fields = {"available_places": ["gte", "lte"]}
