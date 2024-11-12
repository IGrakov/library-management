from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics

from reference_values.models import Genre, Hall, Language
from reference_values.serializers import (
    GenreSerializer,
    HallSerializer,
    LanguageSerializer,
)
from user.permissions import IsAdmin


@extend_schema(
    tags=['language'],
)
class CreateLanguageView(generics.CreateAPIView):
    """Add new language"""

    permission_classes = (IsAdmin,)
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
@extend_schema(
    tags=['language'],
)
class RetrieveUpdateDeleteLanguageView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete language by id"""

    permission_classes = (IsAdmin,)
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()


@extend_schema(
    tags=['language'],
)
class ListLanguageView(generics.ListAPIView):
    """List languages"""

    serializer_class = LanguageSerializer
    queryset = Language.objects.all()


@extend_schema(
    tags=['genre'],
)
class CreateGenreView(generics.CreateAPIView):
    """Add new genre"""

    permission_classes = (IsAdmin,)
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


@extend_schema_view(
    get=extend_schema(
        description='Retrieve genre by id',
    ),
    put=extend_schema(
        description='Update genre by id',
    ),
    patch=extend_schema(
        description='Partially update genre by id',
    ),
    delete=extend_schema(
        description='Delete genre by id',
    ),
)
@extend_schema(
    tags=['genre'],
)
class RetrieveUpdateDeleteGenreView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete genre by id"""

    permission_classes = (IsAdmin,)
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


@extend_schema(
    tags=['genre'],
)
class ListGenreView(generics.ListAPIView):
    """List genres"""

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


@extend_schema(
    tags=['hall'],
)
class CreateHallView(generics.CreateAPIView):
    """Add new hall"""

    permission_classes = (IsAdmin,)
    serializer_class = HallSerializer
    queryset = Hall.objects.all()


@extend_schema_view(
    get=extend_schema(
        description='Retrieve hall by id',
    ),
    put=extend_schema(
        description='Update hall by id',
    ),
    patch=extend_schema(
        description='Partially update hall by id',
    ),
    delete=extend_schema(
        description='Delete hall by id',
    ),
)
@extend_schema(
    tags=['hall'],
)
class RetrieveUpdateDeleteHallView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete hall by id"""

    permission_classes = (IsAdmin,)
    serializer_class = HallSerializer
    queryset = Hall.objects.all()


@extend_schema(
    tags=['hall'],
)
class ListHallView(generics.ListAPIView):
    """List halls"""

    serializer_class = HallSerializer
    queryset = Hall.objects.all()
