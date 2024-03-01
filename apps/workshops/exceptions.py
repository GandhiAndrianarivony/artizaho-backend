from rest_framework.exceptions import APIException
from rest_framework import status


class WorkshopNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Worshop Not Found"


class NoAvailablePlace(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "No More Place Available"


class StatusTypeError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Wrong status code type"
