from django.db.models import QuerySet, Q
from django_filters import rest_framework as filters

from reference_values.models import Hall, Genre, Language


class HallFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Hall
        fields = (
            "name",
        )

class GenreFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Genre
        fields = (
            "name",
        )

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
    def filter_code(queryset: QuerySet[Language], code: str, value: str) -> QuerySet[Language]:
        return queryset.filter(Q(two_letter_code__icontains=value) | Q(three_letter_code__icontains=value)).distinct()
