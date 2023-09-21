from rest_framework.pagination import PageNumberPagination


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 8
    max_page_size = 8
