from rest_framework.exceptions import APIException
from rest_framework import status


class WorkshopNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Worshop Not Found"