"""Custom user"""


from django.contrib.auth import models as m
from django.db import models
from django.apps import apps
from django.contrib.auth.hashers import make_password


class UserManager(m.BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, type, gender, password, **extra_fields):
        """This function is used to create a new user (superuser or no)t

        Args:
            email (str): user email
            type (str): user type (particular or entreprise)
            gender (str): Female, Male or Other
            password (str): user password

        Returns:
            object: recorded user
        """

        if not email:
            raise ValueError("User must have an email address")

        if not type:
            raise ValueError("User must have a type")

        email = self.normalize_email(email)
        # global_user_model = apps.get_model(
        #     self.model._meta.app_label, self.model._meta.object_name
        # )
        user = self.model(email=email, type=type, gender=gender, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, type, gender, password, **extra_fields):
        """Use to create non-admin user
        Return:
            - user (User): An instance of User
        """

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)

        user = self._create_user(email, type, gender, password, **extra_fields)
        return user

    def create_superuser(self, email, type, gender, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        user = self._create_user(email, type, gender, password, **extra_fields)
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

    # [
    #     (MALE, "Male"),
    #     (FEMALE, "Female"),
    #     (OTHER, "Other")
    # ]

    PARTICULAR = "P"
    ENTREPRISE = "E"
    TYPE = {
        PARTICULAR: "Particular",
        ENTREPRISE: "Entreprise",
    }
    # [
    #     (PARTICULAR, "Particular"),
    #     (ENTREPRISE, "Entreprise")
    # ]

    email = models.EmailField(unique=True)
    type = models.CharField(max_length=50, choices=TYPE, db_default=PARTICULAR)
    gender = models.CharField(max_length=10, choices=GENDER, db_default=OTHER)
    dob = models.DateField()

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["type", "gender", "dob"]

    def __str__(self):
        return f"{self.username}"
