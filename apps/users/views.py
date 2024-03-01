"""Module for handling user view"""

from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from apps.authentications.exceptions import NotAuthenticated
from apps.workshops.models import WorkshopReservation
from apps.workshops.serializers import WorkshopReservationSerializer

from api.mixins import ImageMixin
from api import permissions as api_permissions

from .models import User
from .serializers import UserSerializer


class UserViewset(ImageMixin, viewsets.GenericViewSet):
    """Class used for handling request related to user"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        """Method being on the BO to retrieve the list of users"""

        user = request.user
        if user.is_superuser:
            qs = self.get_queryset().filter(is_superuser=False)
            serializer = self.get_serializer(qs, many=True)
            page = self.paginate_queryset(serializer.data)
            if page is not None:
                return self.get_paginated_response(serializer.data)
        else:
            raise NotAuthenticated(detail="Admin authentication required")

    @action(
        methods=["get"],
        detail=False,
        url_path="current-user",
        permission_classes=[permissions.IsAuthenticated],
    )
    def get_current_user(self, request, *args, **kwargs):
        """Get the current user
        Args:
            - request: rest_framework object
        Return:
            - serialized user object
        """
        user = request.user
        return Response(self.get_serializer(user).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """Used for creating a new account
        Args:
            - request: Contains the payload data
        Return:
            - response: rest_framework.Response
        """

        data = request.data
        contacts = data.pop("contacts", None)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.save()

        return Response(
            self.get_serializer(new_user).data, status=status.HTTP_201_CREATED
        )

    @action(
        methods=["delete"],
        detail=False,
        permission_classes=[api_permissions.IsNotAdmin, permissions.IsAuthenticated],
    )
    def remove(self, request, *args, **kwargs):
        """Action being used when user decide to remove his/her account"""

        user = request.user
        self.rm_user(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Action being used by admin to remove/deactivate user accounts"""
        req_user = request.user
        if req_user.is_superuser:
            try:
                user = get_object_or_404(User, pk=pk)
                self.rm_user(user)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except NotAuthenticated as e:
                Response(data={"Warning": f"{e}"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            raise NotAuthenticated(detail="Admin Authentication required")

    def rm_user(self, user):
        user.is_active = False
        user.save()

    @action(
        methods=["patch"],
        detail=False,
        permission_classes=[permissions.IsAuthenticated, api_permissions.IsNotAdmin],
    )
    def update_info(self, request, pk=None, *args, **kwargs):
        """Method used by logged user to update their profile"""

        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    # NOTE: Use UpdateModelMixin.partial to perform partial update

    @action(methods=["get"], detail=False, url_path="admin")
    def get_admin(self, request):
        admins = self.get_queryset().filter(is_superuser=True, is_super_admin=False)

        serializer = self.get_serializer(admins, many=True)
        page = self.paginate_queryset(serializer.data)
        if page is not None:
            return self.get_paginated_response(serializer.data)

    @action(
        methods=["get"],
        detail=False,
        url_path="reservation",
        permission_classes=[permissions.IsAuthenticated],
    )
    def get_user_reservations(self, request, *args, **kwargs):
        """Retrieve all workshop booked by a logged in user"""

        user = request.user
        user_reservation = WorkshopReservation.objects.filter(user=user)

        if user.is_superuser:
            user_reservation = WorkshopReservation.objects.all()
            print(f"[INFO] Admin logged in")

        serialized_data = WorkshopReservationSerializer(
            user_reservation, many=True
        ).data

        page = self.paginate_queryset(serialized_data)
        if page is not None:
            return self.get_paginated_response(serialized_data)
