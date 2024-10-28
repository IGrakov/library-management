from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings

from .models import User
from .serializers import AuthTokenSerializer, UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user un the system"""

    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""

    serializer_class = AuthTokenSerializer
    permission_classes = (AllowAny,)
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id})


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage authenticated user"""

    serializer_class = UserSerializer

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class ListUserView(generics.ListAPIView):
    """Create a new user un the system"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
