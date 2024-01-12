"""Module used to display users information on django admin UI
"""


from django.contrib import admin
from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "username", "type", "gender", "dob")


admin.site.register(models.User, UserAdmin)
# Register your models here.
