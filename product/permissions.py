from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


# class IsAdminOrRead(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return bool(request.user and request.user.is_staff)


class IsAuthenticatedForPutRequests(permissions.BasePermission):
    """
    Custom permission to only allow authenticated users to send PUT requests.
    """

    def has_permission(self, request, view):
        # Allow GET and DELETE requests for any user
        if request.method in SAFE_METHODS or request.method == 'DELETE':
            return True

        # Allow PUT requests only for authenticated users
        if request.method == 'PUT':
            return request.user and request.user.is_authenticated

        return False
