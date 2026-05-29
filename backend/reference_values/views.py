from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from core.pagination import ResultSetPagination
from reference_values.filters import HallFilter, GenreFilter, LanguageFilter
from reference_values.models import Genre, Hall, Language
from reference_values.serializers import (
    GenreSerializer,
    HallSerializer,
    LanguageSerializer,
)
from user.permissions import IsAdminOrReadOnly


@extend_schema(
    tags=["language"],
)
class CreateLanguageView(generics.CreateAPIView):
    """Add new language"""

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()


@extend_schema_view(
    get=extend_schema(
        description="Retrieve language by id",
    ),
    put=extend_schema(
        description="Update language by id",
    ),
    patch=extend_schema(
        description="Partially update language by id",
    ),
    delete=extend_schema(
        description="Delete language by id",
    ),
)
@extend_schema(
    tags=["language"],
)
class RetrieveUpdateDeleteLanguageView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete language by id"""

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()


@extend_schema(
    tags=["language"],
)
class ListLanguageView(generics.ListAPIView):
    """List languages"""

    serializer_class = LanguageSerializer
    queryset = Language.objects.all().order_by("name")
    pagination_class = ResultSetPagination
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_class = LanguageFilter

    ordering_fields = (
        "id",
        "name",
        "two_letter_code",
        "three_letter_code",
    )

    order = "name"


@extend_schema(
    tags=["genre"],
)
class CreateGenreView(generics.CreateAPIView):
    """Add new genre"""

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


@extend_schema_view(
    get=extend_schema(
        description="Retrieve genre by id",
    ),
    put=extend_schema(
        description="Update genre by id",
    ),
    patch=extend_schema(
        description="Partially update genre by id",
    ),
    delete=extend_schema(
        description="Delete genre by id",
    ),
)
@extend_schema(
    tags=["genre"],
)
class RetrieveUpdateDeleteGenreView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete genre by id"""

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


@extend_schema(
    tags=["genre"],
)
class ListGenreView(generics.ListAPIView):
    """List genres"""

    serializer_class = GenreSerializer
    queryset = Genre.objects.all().order_by("name")
    pagination_class = ResultSetPagination
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_class = GenreFilter

    ordering_fields = (
        "id",
        "name",
    )

    order = "name"


@extend_schema(
    tags=["hall"],
)
class CreateHallView(generics.CreateAPIView):
    """Add new hall"""

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = HallSerializer
    queryset = Hall.objects.all()


@extend_schema_view(
    get=extend_schema(
        description="Retrieve hall by id",
    ),
    put=extend_schema(
        description="Update hall by id",
    ),
    patch=extend_schema(
        description="Partially update hall by id",
    ),
    delete=extend_schema(
        description="Delete hall by id",
    ),
)
@extend_schema(
    tags=["hall"],
)
class RetrieveUpdateDeleteHallView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete hall by id"""

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = HallSerializer
    queryset = Hall.objects.all()


@extend_schema(
    tags=["hall"],
)
class ListHallView(generics.ListAPIView):
    """List halls"""

    serializer_class = HallSerializer
    queryset = Hall.objects.all().order_by("name")
    pagination_class = ResultSetPagination
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_class = HallFilter

    ordering_fields = (
        "id",
        "name",
    )

    order = "name"
