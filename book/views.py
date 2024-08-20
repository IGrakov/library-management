from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from book.models import Book
from book.pagination import ResultSetPagination
from book.serializers import BookSerializer


class CreateBookView(generics.CreateAPIView):
    """Create new book"""
    serializer_class = BookSerializer
    queryset = Book.objects.all()


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
