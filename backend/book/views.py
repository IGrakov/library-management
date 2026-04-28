from django.db.models import Count, OuterRef, Subquery, Value, Sum, F
from django.http import HttpResponse
from django.shortcuts import render
from django_filters import rest_framework as filters
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.views import APIView

from book.filters import BookFilter
from book.models import Author, Book, BookCopy
from book.pagination import ResultSetPagination
from book.serializers import (
    AuthorSerializer,
    BookCopySerializer,
    BookSerializer,
    BookWriteSerializer,
)
from user.permissions import IsAdminOrReadOnly


@extend_schema(
    tags=['author'],
)
class CreateAuthorView(generics.CreateAPIView):
    """Create new author"""

    permission_classes = (IsAdminOrReadOnly,)
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

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


@extend_schema(
    tags=['author'],
)
class ListAuthorView(generics.ListAPIView):
    """List authors"""

    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


@extend_schema_view(
    post=extend_schema(
        request=BookWriteSerializer,
        responses={
            status.HTTP_201_CREATED: BookSerializer,
        },
    )
)
class CreateBookView(generics.CreateAPIView):
    """Create new book"""

    permission_classes = (IsAdminOrReadOnly,)
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

    permission_classes = (IsAdminOrReadOnly,)
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BookWriteSerializer
        else:
            return BookSerializer


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name='author',
                description='String that is contained in author last name',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name='language',
                description='Two letter language code',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name='title',
                description='String that is contained in title',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
            ),
        ],
    ),
)
class ListBookView(generics.ListAPIView):
    """List books"""

    queryset = (
        Book.objects
        .prefetch_related('author', 'language', 'genre')
        .annotate(copies_count=Count('copies'))
    )
    serializer_class = BookSerializer
    pagination_class = ResultSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter


@extend_schema(
    tags=['book copy'],
)
class CreateBookCopyView(generics.CreateAPIView):
    """Create new book copy"""

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = BookCopySerializer
    queryset = BookCopy.objects.all()


@extend_schema_view(
    get=extend_schema(
        description='Retrieve book copy by id',
    ),
    delete=extend_schema(
        description='Delete book copy by id',
    ),
)
@extend_schema(
    tags=['book copy'],
)
class RetrieveDeleteBookCopyView(generics.RetrieveDestroyAPIView):
    """Retrieve, update or delete book copy by id"""

    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = BookCopySerializer
    queryset = BookCopy.objects.all()


@extend_schema(
    tags=['book copy'],
)
class ListBookCopyView(generics.ListAPIView):
    """List book copies"""

    serializer_class = BookCopySerializer
    queryset = (
        BookCopy.objects.select_related('book').prefetch_related('book__author', 'book__language', 'book__genre')
    )


def testView(request):
    # query = BookCopy.objects.select_related('book').all().prefetch_related('book__author', 'book__language', 'book__genre')
    # context = {
    #     "query_list": query,
    # }
    # authors = Author.objects.all().order_by('last_name')
    # authors = Author.objects.prefetch_related('books', 'books__copies')
    # authors = Author.objects.annotate(num_of_copies=Count('books__copies')).aggregate(num_of_books=Sum(F('num_of_copies')))
    authors = Author.objects.prefetch_related('books', 'books__copies').annotate(
        num_of_copies=Count('books'),
        num_of_books=Count('books__copies')
    )
    # stats = authors.prefetch_related('books__copies').values('books__copies').annotate(num_of_copies=Count('books__copies')).order_by('-num_of_copies')
    context = {
        'authors': authors,
        # 'stats': stats,
    }

    return render(request, "test.html", context)