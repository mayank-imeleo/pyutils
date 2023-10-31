from rest_framework.pagination import PageNumberPagination


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 8
    max_page_size = 8


class PageNumberPagination20(PageNumberPagination):
    page_size = 20
    max_page_size = 20


class PageNumberPagination30(PageNumberPagination):
    page_size = 30
    max_page_size = 30
