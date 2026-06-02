from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny

from book.filters import BookFilter
from book.models import Book, BookCopy
from book.serializers import (
    BookCopySerializer,
    BookSerializer,
    BookWriteSerializer,
)
from core.pagination import ResultSetPagination
from user.permissions import IsAdminOrReadOnly


@extend_schema_view(
    post=extend_schema(
        request=BookWriteSerializer,
        responses={
            status.HTTP_201_CREATED: BookSerializer,
        },
    ),
)
class CreateBookView(generics.CreateAPIView):
    """Create new book"""

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = BookSerializer
    queryset = Book.objects.all()


@extend_schema_view(
    get=extend_schema(
        description="Retrieve book by id",
    ),
    put=extend_schema(
        description="Update book by id",
    ),
    patch=extend_schema(
        description="Partially update book by id",
    ),
    delete=extend_schema(
        description="Delete book by id",
    ),
)
class RetrieveUpdateDeleteBookView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete book by id"""

    permission_classes = (IsAdminOrReadOnly,)
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return BookWriteSerializer
        return BookSerializer


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name="author",
                description="String that is contained in author last name",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="language",
                description="Two letter language code",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="title",
                description="String that is contained in title",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
        ],
    ),
)
class ListBookView(generics.ListAPIView):
    """List books"""

    queryset = Book.objects.prefetch_related("author", "language", "genre").annotate(copies_count=Count("copies"))
    serializer_class = BookSerializer
    pagination_class = ResultSetPagination
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    filterset_class = BookFilter
    permission_classes = (AllowAny,)

    ordering_fields = (
        "title",
        "published_date",
        "pages",
        "isbn",
        "copies_count",
    )

    order = "title"


@extend_schema(
    tags=["book copy"],
)
class CreateBookCopyView(generics.CreateAPIView):
    """Create new book copy"""

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = BookCopySerializer
    queryset = BookCopy.objects.all()


@extend_schema_view(
    get=extend_schema(
        description="Retrieve book copy by id",
    ),
    delete=extend_schema(
        description="Delete book copy by id",
    ),
)
@extend_schema(
    tags=["book copy"],
)
class RetrieveDeleteBookCopyView(generics.RetrieveDestroyAPIView):
    """Retrieve, update or delete book copy by id"""

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = BookCopySerializer
    queryset = BookCopy.objects.all()


@extend_schema(
    tags=["book copy"],
)
class ListBookCopyView(generics.ListAPIView):
    """List book copies"""

    serializer_class = BookCopySerializer
    queryset = BookCopy.objects.select_related("book").prefetch_related("book__author", "book__language", "book__genre")
    pagination_class = ResultSetPagination
