from django.db.models import Q
from django_filters import rest_framework as filters

from book.models import Book


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    author = filters.CharFilter(method='filter_author')
    publication_year = filters.NumberFilter(field_name='published_date__year', lookup_expr='exact')
    language = filters.CharFilter(field_name='language__name', lookup_expr='icontains')
    genre = filters.CharFilter(field_name='genre__name', lookup_expr='icontains')
    isbn= filters.CharFilter(field_name='isbn', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year', 'language', 'genre']

    @staticmethod
    def filter_author(queryset, name, value):
        """Filter books by any part of author name"""
        return queryset.filter(
            Q(author__first_name__icontains=value) |
            Q(author__middle_name__icontains=value) |
            Q(author__last_name__icontains=value)
        ).distinct()
