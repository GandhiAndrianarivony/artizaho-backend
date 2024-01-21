from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import User


class CustomUserSession(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")
    session_key = models.CharField(_("session_key"), max_length=40)
    expires_at = models.DateTimeField(_("expires_at"))
