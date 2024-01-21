"""Common class/function used by some applications"""

from rest_framework import permissions


class PermissionMixin:
    permission_classes = [
        permissions.IsAuthenticated
    ]