from rest_framework import permissions

from user import constants


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.method in permissions.SAFE_METHODS
            or request.user.groups.filter(name=constants.Roles.ADMIN).exists()
        ):
            return True
