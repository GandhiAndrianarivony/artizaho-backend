from rest_framework import serializers

from apps.images.serializers import ImageSerializer

from .models import Artisan


class ArtisanSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Artisan
        fields = "__all__"

    def get_images(self, instance: Artisan):
        images = instance.images.all()
        return ImageSerializer(images, many=True).data
