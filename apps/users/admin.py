"""Module used to display users information on django admin UI
"""


from django.contrib import admin
from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "account_type",
        "gender",
        "dob",
        "nif",
        "is_staff",
    )


admin.site.register(models.User, UserAdmin)
# Register your models here.
