"""Serializer module is used to serialize user model or python dictionaries"""
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Used to serialize user model or python dictionaries

    Attributes:

    Methods:
    """

    class Meta:
        model = User
        fields = "__all__"

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
        # return User.objects.create(**validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password is not None:
            instance.password = make_password(password)
            instance.save()
        return super().update(instance, validated_data)


class UserInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "groups", "user_permissions"]