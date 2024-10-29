from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics

from reference_values.models import Language
from reference_values.serializers import LanguageSerializer


class CreateLanguageView(generics.CreateAPIView):
    """Add new language"""

    serializer_class = LanguageSerializer
    queryset = Language.objects.all()


@extend_schema_view(
    get=extend_schema(
        description='Retrieve language by id',
    ),
    put=extend_schema(
        description='Update language by id',
    ),
    patch=extend_schema(
        description='Partially update language by id',
    ),
    delete=extend_schema(
        description='Delete language by id',
    ),
)
class RetrieveUpdateDeleteLanguageView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete language by id"""

    serializer_class = LanguageSerializer
    queryset = Language.objects.all()


class ListLanguageView(generics.ListAPIView):
    """List languages"""

    serializer_class = LanguageSerializer
    queryset = Language.objects.all()
