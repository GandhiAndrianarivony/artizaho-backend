from rest_framework.exceptions import APIException
from rest_framework import status


class NotMatched(APIException):
    default_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Logged user could not modify the specified pk user"


class NumberOfImageNotAllowed(APIException):
    default_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Multiple image uploaded"


