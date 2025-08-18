from rest_framework.pagination import PageNumberPagination


class Page(PageNumberPagination):
    page_size = 1