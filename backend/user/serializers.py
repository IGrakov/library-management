from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from user import constants


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""
    role = serializers.ChoiceField(
        choices=[constants.Roles.READER, constants.Roles.LIBRARIAN],
        write_only=True
    )

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
            'role',
        ]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""

        role = validated_data.pop('role')
        request = self.context['request']
        creator = request.user

        if role == constants.Roles.LIBRARIAN:
            if not creator.groups.filter(name=constants.Roles.ADMIN).exists():
                raise serializers.ValidationError("Only admin can create librarian")

        elif role == constants.Roles.READER:
            if not creator.groups.filter(name=constants.Roles.LIBRARIAN).exists():
                raise serializers.ValidationError("Only librarian can create regular users")

        else:
            raise serializers.ValidationError("Invalid role")

        user = get_user_model().objects.create_user(**validated_data)

        if role:
            group = Group.objects.get(name=role)
            user.groups.clear()
            user.groups.add(group)

            if role == constants.Roles.LIBRARIAN:
                user.is_staff = True

        user.save()

        return user

    def update(self, instance, validated_data):
        """Update a user and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

    def get_role(self, obj):
        if obj.is_superuser:
            return 'superuser'
        group = obj.groups.first()
        return group.name if group else None


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""

    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False, write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        """Validate and authenticate user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), username=email, password=password)
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
