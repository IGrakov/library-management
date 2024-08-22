from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema

from book.models import Book
from book.pagination import ResultSetPagination
from book.serializers import BookSerializer


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
    )
)
class RetrieveUpdateDeleteBookView(
    generics.RetrieveAPIView,
    generics.UpdateAPIView,
    generics.DestroyAPIView,
):
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
