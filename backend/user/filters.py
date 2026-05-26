from django.db.models import Q, QuerySet
from django_filters import rest_framework as filters

from user.models import User


class UserFilter(filters.FilterSet):
    name = filters.CharFilter(method="filter_name")
    email = filters.CharFilter(field_name="email", lookup_expr="icontains")
    role = filters.CharFilter(
        field_name="groups__name",
        lookup_expr="icontains",
    )

    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "role",
        )

    @staticmethod
    def filter_name(queryset: QuerySet[User], name: str, value: str) -> QuerySet[User]:  # noqa: ARG004
        """Filter user by any part of user name"""
        return queryset.filter(Q(first_name__icontains=value) | Q(last_name__icontains=value)).distinct()
