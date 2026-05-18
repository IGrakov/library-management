from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from user import constants
from user.models import User


def get_user_role_rank(user: User) -> int:
    if not user.is_active:
        return constants.INACTIVE_USER_RANK  # disabled user has no rights

    if user.is_superuser:
        return constants.SUPER_USER_RANK  # should be the highest rank

    if user.groups.filter(name=constants.Roles.ADMIN).exists():
        return constants.ADMIN_USER_RANK

    if user.groups.filter(name=constants.Roles.LIBRARIAN).exists():
        return constants.LIBRARIAN_USER_RANK

    return constants.READER_USER_RANK


class IsAuthenticatedAndActive(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:  # noqa: ARG002
        return request.user and request.user.is_authenticated and request.user.is_active


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:  # noqa: ARG002
        if not request.user.is_authenticated or not request.user.is_active:
            return False

        if request.user.is_superuser or request.user.groups.filter(name=constants.Roles.ADMIN).exists():
            return True

        return False


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:  # noqa: ARG002
        if not request.user.is_authenticated or not request.user.is_active:
            return False

        if (
            request.user.is_superuser
            or request.user.groups.filter(name=constants.Roles.ADMIN).exists()
            or request.method in permissions.SAFE_METHODS
        ):
            return True

        return False


class IsLibrarian(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:  # noqa: ARG002
        if (
            request.user.is_authenticated
            and request.user.is_active
            and request.user.groups.filter(name=constants.Roles.LIBRARIAN).exists()
        ):
            return True

        return False


class IsLibrarianOrAdmin(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:  # noqa: ARG002
        if not request.user.is_authenticated or not request.user.is_active:
            return False

        if request.user.is_superuser:
            return True

        return request.user.groups.filter(name__in={constants.Roles.ADMIN, constants.Roles.LIBRARIAN}).exists()


class CanCreateOrManageUser(IsAuthenticatedAndActive):
    def has_object_permission(self, request: Request, view: APIView, obj: User) -> bool:  # noqa: ARG002
        actor = request.user

        # any actor despite his rank must be active
        if not actor.is_active:
            return False

        # no one, even superuser, can perform any actions with superuser
        if obj.is_superuser:
            return False

        # superuser override and can perform actions with deleted (not active) users
        if actor.is_superuser:
            return True

        # cannot interact with inactive targets
        if not obj.is_active:
            return False

        # self access always allowed
        if obj == actor:
            return True

        actor_rank = get_user_role_rank(actor)
        target_rank = get_user_role_rank(obj)

        # only higher rank user can manage lower rank user, i.e.
        # admin cannot manage another admin
        # librarian cannot manage another librarian
        return actor_rank > target_rank
