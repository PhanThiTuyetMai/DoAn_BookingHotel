from rest_framework import pagination


class PagePaginator(pagination.PageNumberPagination):
    page_size = 5


class RoomPagePaginator(pagination.PageNumberPagination):
    page_size = 2