from typing import Any, ClassVar

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from user import constants
from user.models import User
from user.permissions import get_user_role_rank


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    role = serializers.ChoiceField(
        choices=[constants.Roles.READER, constants.Roles.LIBRARIAN, constants.Roles.ADMIN],
        write_only=True,
    )

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
        )
        extra_kwargs: ClassVar = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data: dict[str, Any]) -> User:
        """Create a new user with encrypted password and return it"""

        role = validated_data.pop("role")
        request = self.context["request"]
        creator = request.user

        if role == constants.Roles.LIBRARIAN:
            if get_user_role_rank(creator) < constants.ADMIN_USER_RANK:
                raise serializers.ValidationError("Only admin can create librarian")  # noqa: EM101, TRY003

        elif role == constants.Roles.READER:
            if get_user_role_rank(creator) < constants.LIBRARIAN_USER_RANK:
                raise serializers.ValidationError("Only librarian or admin can create regular users")  # noqa: EM101, TRY003

        else:
            raise serializers.ValidationError("Invalid role")  # noqa: EM101, TRY003

        user = get_user_model().objects.create_user(**validated_data)

        if role:
            group = Group.objects.get(name=role)
            user.groups.clear()
            user.groups.add(group)

            if role in {constants.Roles.LIBRARIAN, constants.Roles.ADMIN}:
                user.is_staff = True

        user.save()

        return user

    def update(self, instance: User, validated_data: dict[str, Any]) -> User:
        """Update a user and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

    def get_role(self, obj: User) -> str | None:
        if obj.is_superuser:
            return "superuser"
        group = obj.groups.first()
        return group.name if group else None


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""

    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"}, trim_whitespace=False, write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Validate and authenticate user"""
        email = attrs.get("email")
        password = attrs.get("password")

        user: AbstractBaseUser | None = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code="authentication")

        attrs["user"] = user
        return attrs
