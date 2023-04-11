from rest_framework import permissions


class IsNotAuthenticated(permissions.BasePermission):
    """
    Global permission to check user authentication status.
    You can block access to some urls for authenticated
    users.
    """

    def has_permission(self, request, view):
        if request in permissions.SAFE_METHODS:
            return True

        return bool(not request.user.is_authenticated)
