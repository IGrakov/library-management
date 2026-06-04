from django.db.models import QuerySet, Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter

from core.constants import MAX_NUM_OF_ITEMS_IN_LOOKUP
from core.pagination import ResultSetPagination
from reference_values.filters import GenreFilter, HallFilter, LanguageFilter, AuthorFilter
from reference_values.models import Author, Genre, Hall, Language
from reference_values.serializers import (
    AuthorSerializer,
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


@extend_schema(
    tags=["author"],
)
class CreateAuthorView(generics.CreateAPIView):
    """Create new author"""

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


@extend_schema_view(
    get=extend_schema(
        description="Retrieve author by id",
    ),
    put=extend_schema(
        description="Update author by id",
    ),
    patch=extend_schema(
        description="Partially update author by id",
    ),
    delete=extend_schema(
        description="Delete author by id",
    ),
)
@extend_schema(
    tags=["author"],
)
class RetrieveUpdateDeleteAuthorView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete author by id"""

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


@extend_schema(
    tags=["author"],
)
class ListAuthorView(generics.ListAPIView):
    """List authors"""

    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    pagination_class = ResultSetPagination
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )

    filterset_class = AuthorFilter

    ordering_fields = (
        "id",
        "last_name",
    )

    order = "last_name"


@extend_schema(
    tags=["author"],
)
class AuthorLookupView(generics.ListAPIView):
    """Lookup for authors"""

    serializer_class = AuthorSerializer
    def get_queryset(self):
        search = self.request.query_params.get("search")

        if not search:
            return Author.objects.none()

        return (
            Author.objects.filter(
                Q(last_name__icontains=search)
                | Q(first_name__icontains=search)
                | Q(middle_name__icontains=search)
            )
            .order_by("last_name")[:MAX_NUM_OF_ITEMS_IN_LOOKUP]
        )
