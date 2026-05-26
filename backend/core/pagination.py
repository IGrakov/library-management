from rest_framework.pagination import PageNumberPagination

from core.constants import NUM_OF_ITEMS_PER_PAGE


class ResultSetPagination(PageNumberPagination):
    page_size = NUM_OF_ITEMS_PER_PAGE
