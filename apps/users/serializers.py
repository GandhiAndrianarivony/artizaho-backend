"""Serializer module is used to serialize user model or python dictionaries"""
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer

from apps.images.serializers import ImageSerializer
from apps.contacts.serializers import ContactSerializer

from .models import User


@extend_schema_serializer(
    exclude_fields=(
        "user_permissions",
        "groups",
        "is_staff",
        "is_active",
        "date_joined",
    )
)
class UserSerializer(serializers.ModelSerializer):
    """Used to serialize user model or python dictionaries

    Attributes:

    Methods:
    """

    images = ImageSerializer(many=True) # serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = "__all__"
        private_fields = [
            "password",
            "last_login",
            "is_superuser",
            "is_staff",
            "groups",
            "user_permissions",
        ]

    def validate(self, data):
        """Custom data validation before saving data

        Args:
            - data: is the request data

        Return:
            - data: is the request data
        """

        account_type = data.get("account_type")
        nif = data.get("nif", None)
        if account_type == "E" and nif is None:
            raise serializers.ValidationError(
                {"account_type": "Account of type Entreprise (E) should have NIF STAT"}
            )

        return data

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password is not None:
            instance.password = make_password(password)
            instance.save()
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        repr = super().to_representation(instance)

        for field in self.Meta.private_fields:
            repr.pop(field, None)

        return repr

    # def get_images(self, instance: User):
    #     images = instance.images.all()
    #     return ImageSerializer(images, many=True).data
