"""Custom user"""

from enum import Enum

from django.contrib.auth import models as m
from django.db import models
from django.apps import apps
from django.contrib.auth.hashers import make_password


class UserManager(m.BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, account_type, password, **extra_fields):
        """This function is used to create a new user (superuser or no)t

        Args:
            email (str): user email
            account_type (str): user account_type (particular or entreprise)
            password (str): user password

        Returns:
            object: recorded user
        """

        if not email:
            raise ValueError("User must have an email address")

        if not account_type:
            raise ValueError("User must have a account_type")

        email = self.normalize_email(email)
        # global_user_model = apps.get_model(
        #     self.model._meta.app_label, self.model._meta.object_name
        # )
        user = self.model(email=email, account_type=account_type, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, account_type, password, **extra_fields):
        """Use to create non-admin user
        Return:
            - user (User): An instance of User
        """

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)

        user = self._create_user(email, account_type, password, **extra_fields)
        return user

    def create_superuser(self, email, account_type, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        user = self._create_user(email, account_type, password, **extra_fields)
        return user


# Create custom user model
class User(m.AbstractUser):
    """Custom user model

    Attributes:
        - email: The email address
        - type: The user type
        - gender: The user gender
    """

    MALE = "M"
    FEMALE = "F"
    OTHER = "O"
    GENDER = {
        MALE: "Male",
        FEMALE: "Female",
        OTHER: "Other",
    }

    PARTICULAR = "P"
    ENTREPRISE = "E"
    TYPE = {
        PARTICULAR: "Particular",
        ENTREPRISE: "Entreprise",
    }
    username = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True)
    account_type = models.CharField(max_length=50, choices=TYPE, db_default=PARTICULAR)
    gender = models.CharField(max_length=10, choices=GENDER, db_default=OTHER)
    dob = models.DateField(null=True)
    nif = models.TextField(null=True)
    phone_number = models.CharField(max_length=255, null=True)
    is_super_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["account_type", "is_super_admin"]

    def __str__(self):
        return f"{self.username}"
