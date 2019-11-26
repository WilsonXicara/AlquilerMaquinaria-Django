"""
Users permissions.
"""
# Django REST Framework
from rest_framework.permissions import BasePermission

class IsSuperUserPermission(BasePermission):
    """
    Verify requesting user is superuser.
    """

    def has_permission(self, request, view):
        """
        Verify requesting user is superuser.
        """
        return request.user.is_superuser