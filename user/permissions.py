from rest_framework import permissions

from user import constants


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and (
            request.method in permissions.SAFE_METHODS
            or request.user.groups.filter(name=constants.Roles.ADMIN).exists()
        ):
            return True


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.groups.filter(name=constants.Roles.ADMIN).exists():
            return True


class IsLibrarianOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and (
            request.method in permissions.SAFE_METHODS
            or request.user.groups.filter(name=constants.Roles.LIBRARIAN).exists()
        ):
            return True


class IsLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.groups.filter(name=constants.Roles.LIBRARIAN).exists():
            return True
