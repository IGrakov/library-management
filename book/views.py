from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics

from book.filters import BookFilter
from book.models import Author, Book
from book.pagination import ResultSetPagination
from book.serializers import AuthorSerializer, BookSerializer, BookWriteSerializer
from user.permissions import IsAdmin


@extend_schema(
    tags=['author'],
)
class CreateAuthorView(generics.CreateAPIView):
    """Create new author"""

    permission_classes = (IsAdmin,)
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


@extend_schema_view(
    get=extend_schema(
        description='Retrieve author by id',
    ),
    put=extend_schema(
        description='Update author by id',
    ),
    patch=extend_schema(
        description='Partially update author by id',
    ),
    delete=extend_schema(
        description='Delete author by id',
    ),
)
@extend_schema(
    tags=['author'],
)
class RetrieveUpdateDeleteAuthorView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete author by id"""

    permission_classes = (IsAdmin,)
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


@extend_schema(
    tags=['author'],
)
class ListAuthorView(generics.ListAPIView):
    """List authors"""

    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


class CreateBookView(generics.CreateAPIView):
    """Create new book"""

    permission_classes = (IsAdmin,)
    serializer_class = BookWriteSerializer
    queryset = Book.objects.all()


@extend_schema_view(
    get=extend_schema(
        description='Retrieve book by id',
    ),
    put=extend_schema(
        description='Update book by id',
    ),
    patch=extend_schema(
        description='Partially update book by id',
    ),
    delete=extend_schema(
        description='Delete book by id',
    ),
)
class RetrieveUpdateDeleteBookView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete book by id"""

    permission_classes = (IsAdmin,)
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BookWriteSerializer
        else:
            return BookSerializer


class ListBookView(generics.ListAPIView):
    """List books"""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = ResultSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter
