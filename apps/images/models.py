import pathlib

from django.db import models

from apps.users.models import User
from apps.artisans.models import Artisan
from apps.workshops.models import Workshop


def upload_to(instance, filename):
    fd = instance.folder_name
    fn = instance.file_name
    ext = pathlib.Path(filename).suffix
    return f"{fd}/{fn}{ext}"


class Image(models.Model):
    folder_name = models.CharField(max_length=50)
    file_name = models.CharField(max_length=255)
    image_url = models.ImageField(upload_to=upload_to)
    base_url = models.TextField(null=True)
    blurhash_code = models.CharField(max_length=255, null=True)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="images", null=True
    )
    artisan = models.ForeignKey(
        Artisan, on_delete=models.CASCADE, related_name="images", null=True
    )
    workshop = models.ForeignKey(
        Workshop, on_delete=models.CASCADE, related_name="images", null=True
    )
