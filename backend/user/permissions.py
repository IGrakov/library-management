from rest_framework import permissions

from user import constants


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and (
            request.method in permissions.SAFE_METHODS
            or request.user.groups.filter(name=constants.Roles.ADMIN).exists()
        ):
            return True

        return False


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.groups.filter(name=constants.Roles.ADMIN).exists():
            return True

        return False


class IsLibrarianOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and (
            request.method in permissions.SAFE_METHODS
            or request.user.groups.filter(name=constants.Roles.LIBRARIAN).exists()
        ):
            return True

        return False


class IsLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.groups.filter(name=constants.Roles.LIBRARIAN).exists():
            return True

        return False


class IsSelfOrLibrarianOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if request.user.groups.filter(name=constants.Roles.ADMIN).exists():
            return True

        if request.user.groups.filter(name=constants.Roles.LIBRARIAN).exists():
            return True

        return obj == request.user
