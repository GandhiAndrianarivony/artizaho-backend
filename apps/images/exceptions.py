"""Custom exception for images apps"""

from rest_framework.exceptions import APIException
from rest_framework import status


class MissingImage(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "No image founded"


class AppNameNotFound(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "App Name not found"


class TruncatedImage(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Image truncated"