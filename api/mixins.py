"""Common class/function used by some applications"""

import uuid
from typing import List
from enum import Enum

import blurhash
from PIL import Image as pil_image

from rest_framework import status
from rest_framework.response import Response
from django.apps import apps
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework.decorators import action

from apps.images.models import Image
from apps.images import exceptions as image_exceptions
from api.configs import mapping
from apps.users import exceptions as user_exceptions
from apps.users.models import User
from apps.artisans.models import Artisan
from apps.authentications import exceptions as auth_exceptions

from . import utils


APP_NAMES = [
    config.name.split(".")[-1]
    for config in apps.get_app_configs()
    if config.name.split(".")[0] == "apps"
]


class IndividualType(str, Enum):
    USER = "user"
    ARTISAN = "artisan"

    @classmethod
    def list(cls):
        return list(map(lambda x: x.value, cls))


class ImageMixin:
    """All viewset which implement the updload_image function inherite this class

    Method:
        - create_image (folder_name) -> Image: create an image to the database
    """

    config = mapping.MapConfiguration()

    def check_individual(self, user, uploaded_images, instance):
        # Check if user is authenticated
        if not user.is_authenticated:
            raise auth_exceptions.NotAuthenticated(detail="Authentication required")

        # Check mismatching between pk and user's logged id
        if self.basename == IndividualType.USER.value and user.id != int(
            self.kwargs.get("pk")
        ):
            raise user_exceptions.NotMatched(
                detail="Mismatching between logged using and pk"
            )

        # Check number of uploaded images
        if self.basename in IndividualType.list() and (
            len(uploaded_images) > 1 or len(uploaded_images) == 0
        ):
            raise user_exceptions.NumberOfImageNotAllowed(
                detail="Image file not founded or Multiple file uploaded"
            )

        if isinstance(instance, (User, Artisan)):
            instance.images.clear()

    def get_app_name(self):
        return utils.to_plural(self.basename)

    @action(methods=["post"], detail=True)
    def upload_image(self, request, pk=None, *args, **kwargs):
        # Get the user logged in
        user = request.user

        # Get list of uploaded images
        uploaded_images = request.FILES.getlist("images")

        # Get django application name
        app_name = self.get_app_name()

        # Get the django model
        model = apps.get_model(
            app_label=app_name,
            model_name=self.config.get_model_name_from_apps_name(app_name),
        )

        # Instantiate model
        instance = get_object_or_404(model, pk=pk)

        # CHECKING
        self.check_individual(user, uploaded_images, instance)

        with transaction.atomic():
            existing_images_filename = list(
                Image.objects.values_list("file_name", flat=True)
            )
            existing_blurhashes_code = list(
                Image.objects.values_list("blurhash_code", flat=True)
            )

            # Create each image from list of images
            for uploaded_image_url in uploaded_images:
                image_obj = self.create_image(
                    app_name,
                    uploaded_image_url,
                    existing_images_filename,
                    existing_blurhashes_code,
                )
                if image_obj:
                    instance.images.add(image_obj)
                    image_obj.save()

        return Response(status=status.HTTP_201_CREATED)

    def create_image(
        self,
        app_name: str,
        uploaded_image_url: InMemoryUploadedFile,
        existing_images_filename: List[str],
        existing_blurhashes_code: List[str],
    ):
        if app_name in APP_NAMES:
            hash_code = self.get_blurhash_code(uploaded_image_url)

            # FIXME: How to handle duplicate image?
            # # Check if image is already created based on hash_code
            # if hash_code in existing_blurhashes_code:
            #     return Image.objects.none()
            # else:

            new_file_name = str(uuid.uuid4())

            # Generate new filename
            while new_file_name in existing_images_filename:
                new_file_name = str(uuid.uuid4())

            # Create and save image to db
            new_image = Image.objects.create(
                folder_name=app_name,
                file_name=new_file_name,
                image_url=uploaded_image_url,
                blurhash_code=hash_code,
            )
            new_image.save()

            # Append new hash code and new filename
            existing_images_filename.append(new_file_name)
            existing_blurhashes_code.append(hash_code)

            return new_image
        else:
            raise image_exceptions.AppNameNotFound(detail="Wrong url")

    def get_blurhash_code(self, img_path: InMemoryUploadedFile):
        """Generate blurhash of image

        Arguments:
            - img_path (InMemoryUploadedFile): uploaded_image
        """
        image = self.read_image(img_path)
        return blurhash.encode(image, x_components=4, y_components=3)

    @staticmethod
    def read_image(path: InMemoryUploadedFile):
        return pil_image.open(path)
