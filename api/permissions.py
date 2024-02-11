"""Custom permision"""
from rest_framework import permissions


class IsNotAdmin(permissions.BasePermission):
    """Custom permission to deny access to admin users"""

    def has_permission(self, request, view):
        return not request.user.is_staff


class AllowListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == "list" or request.method == "GET":
            return True
        else:
            return request.user and request.user.is_superuser