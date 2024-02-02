from rest_framework.exceptions import APIException
from rest_framework import status


class ArtisanNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Artisan not found"