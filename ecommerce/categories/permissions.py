from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission to allow admins operations with categories.
    Users without staff status can only see categories.
    """

    def has_permission(self, request, view):
        if request in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
