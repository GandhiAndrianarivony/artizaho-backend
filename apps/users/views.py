"""Module for handling user view"""

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer, UserInstanceSerializer


class UserViewset(viewsets.GenericViewSet):
    """Class used for handling request related to user"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """Used for creating a new account
        Args:
            - request: Contains the payload data
        Return:
            - response: rest_framework.Response
        """
        # breakpoint()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = User.objects.create_user(**serializer.data)

        return Response(
            UserInstanceSerializer(new_user).data, status=status.HTTP_201_CREATED
        )
