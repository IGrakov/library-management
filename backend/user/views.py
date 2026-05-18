from typing import Any

from django.db.models import Q, QuerySet
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.settings import api_settings

from . import constants
from .models import User
from .permissions import CanCreateOrManageUser, IsLibrarianOrAdmin, get_user_role_rank
from .serializers import AuthTokenSerializer, UserSerializer


class CreateUserView(generics.CreateAPIView):
    """
    Create a new user in the system.
    Permitted only to admins to create librarians and to librarians to create readers
    """

    serializer_class = UserSerializer
    permission_classes = (CanCreateOrManageUser,)


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""

    serializer_class = AuthTokenSerializer
    permission_classes = (AllowAny,)
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request: Request, *args: Any, **kwargs: Any):  # noqa: ARG002, ANN401
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.id})


@extend_schema_view(
    get=extend_schema(
        description="Retrieve user by id",
    ),
    put=extend_schema(
        description="Update user by id",
    ),
    patch=extend_schema(
        description="Partially update user by id",
    ),
)
class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage authenticated user. Permitted only to self or librarians"""

    serializer_class = UserSerializer
    permission_classes = (CanCreateOrManageUser,)

    def get_object(self) -> User:
        """Retrieve and return authenticated user"""
        pk = self.kwargs.get("pk")

        obj = self.request.user if pk is None else User.objects.get(pk=pk)

        self.check_object_permissions(self.request, obj)
        return obj


class ListUserView(generics.ListAPIView):
    """List users in the system. Permitted only to librarians"""

    serializer_class = UserSerializer
    permission_classes = (IsLibrarianOrAdmin,)

    def get_queryset(self) -> QuerySet[User]:
        user = self.request.user

        # Superuser sees everything
        if user.is_superuser:
            return User.objects.all()

        # Admin / Librarian see only lower-ranked active users
        actor_rank = get_user_role_rank(user)

        return User.objects.filter(is_active=True).filter(self._lower_rank_q(actor_rank))

    def _lower_rank_q(self, actor_rank: int) -> Q:
        if actor_rank == constants.ADMIN_USER_RANK:
            # admin sees librarians + readers
            return Q(groups__name=constants.Roles.LIBRARIAN) | Q(groups__name=constants.Roles.READER)

        if actor_rank == constants.LIBRARIAN_USER_RANK:
            # librarian sees only readers
            return Q(groups__name=constants.Roles.READER)

        return Q(pk=None)  # readers see nothing
