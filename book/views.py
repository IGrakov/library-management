from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics

from book.models import Author, Book
from book.pagination import ResultSetPagination
from book.serializers import AuthorSerializer, BookSerializer


class CreateAuthorView(generics.CreateAPIView):
    """Create new author"""

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
class RetrieveUpdateDeleteAuthorView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete author by id"""

    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


class ListAuthorView(generics.ListAPIView):
    """List authors"""

    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


class CreateBookView(generics.CreateAPIView):
    """Create new book"""

    serializer_class = BookSerializer
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

    serializer_class = BookSerializer
    queryset = Book.objects.all()


class ListBookView(generics.ListAPIView):
    """List books"""

    serializer_class = BookSerializer
    queryset = Book.objects.all()
    pagination_class = ResultSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'published_date', 'language']
