"""Module for handling user view"""

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin

from .models import User
from .serializers import UserSerializer, UserInstanceSerializer
from apps.authentications.exceptions import NotAuthenticated


class UserViewset(
    UpdateModelMixin,
    viewsets.GenericViewSet
):
    """Class used for handling request related to user"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            qs = self.get_queryset()
            serializer = self.get_serializer(qs, many=True)
            page = self.paginate_queryset(serializer.data)
            if page is not None:
                return self.get_paginated_response(serializer.data)
        else:
            raise NotAuthenticated(detail="Admin authentication required")

    @action(methods=["get"], detail=False)
    def current_user(self, request, *args, **kwargs):
        """Get the current user
        Args:
            - request: rest_framework object
        Return:
            - serialized user object
        """
        user = request.user
        if user.is_authenticated:
            return Response(
                UserInstanceSerializer(user).data, status=status.HTTP_200_OK
            )
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

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
        new_user = serializer.save()

        return Response(
            UserInstanceSerializer(new_user).data, status=status.HTTP_201_CREATED
        )

    @action(methods=["get"], detail=False)
    def remove(self, request, pk=None):
        """Action being used when user decide to remove his/her account"""
        user = request.user
        if user.is_authenticated:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise NotAuthenticated(detail="Authentication required")

    def destroy(self, request, pk=None):
        """Action being used by admin to remove user accounts"""
        user = request.user
        if user.is_superuser:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise NotAuthenticated(detail="Admin Authentication required")

    # NOTE: Use UpdateModelMixin.partial to perform partial update
        
    # def partial_update(self, request, pk=None, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(status=status.HTTP_200_OK)

    # TODO: Updload image for a given user