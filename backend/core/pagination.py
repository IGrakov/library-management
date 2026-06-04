from rest_framework.pagination import PageNumberPagination

from core.constants import MAX_NUM_OF_ITEMS_PER_PAGE, NUM_OF_ITEMS_PER_PAGE


class ResultSetPagination(PageNumberPagination):
    page_size = NUM_OF_ITEMS_PER_PAGE

    page_size_query_param = "page_size"
    max_page_size = MAX_NUM_OF_ITEMS_PER_PAGE
