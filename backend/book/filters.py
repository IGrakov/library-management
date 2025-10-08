from django_filters import rest_framework as filters

from book.models import Book


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    author = filters.CharFilter(field_name='author__last_name', lookup_expr='icontains')
    publication_year = filters.NumberFilter(field_name='published_date__year', lookup_expr='exact')
    language = filters.CharFilter(field_name='language__two_letter_code', lookup_expr='exact')

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'language']
