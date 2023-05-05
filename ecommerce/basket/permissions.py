from rest_framework import permissions
from basket.utils import BasketMixin


class BasketLenMoreThanZeroPermission(BasketMixin, permissions.BasePermission):
    """
    Permission that allows access only if the user
    has at least one item in his basket.
    """
    message = 'You dont have items in your basket!'

    def has_permission(self, request, view):
        if request in permissions.SAFE_METHODS:
            return True
        return bool(self.get_basket_len(request) > 0)
