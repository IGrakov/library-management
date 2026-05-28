from django_filters import rest_framework as filters

from reference_values.models import Hall


class HallFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Hall
        fields = (
            "name",
        )
