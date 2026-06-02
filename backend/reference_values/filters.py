from django.db.models import Q, QuerySet
from django_filters import rest_framework as filters

from reference_values.models import Author, Genre, Hall, Language


class HallFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Hall
        fields = ("name",)


class GenreFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Genre
        fields = ("name",)


class LanguageFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    code = filters.CharFilter(method="filter_code")

    class Meta:
        model = Language
        fields = (
            "name",
            "code",
        )

    @staticmethod
    def filter_code(queryset: QuerySet[Language], code: str, value: str) -> QuerySet[Language]:  # noqa: ARG004
        return queryset.filter(Q(two_letter_code__icontains=value) | Q(three_letter_code__icontains=value)).distinct()


class AuthorFilter(filters.FilterSet):
    """Filter author by any part of author name"""

    name = filters.CharFilter(method="filter_name")

    class Meta:
        model = Author
        fields = ("name",)

    @staticmethod
    def filter_name(queryset: QuerySet[Author], code: str, value: str) -> QuerySet[Author]:  # noqa: ARG004
        return queryset.filter(
            Q(author__first_name__icontains=value)
            | Q(author__middle_name__icontains=value)
            | Q(author__last_name__icontains=value),
        ).distinct()
