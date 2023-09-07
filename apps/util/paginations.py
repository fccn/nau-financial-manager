from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ShortResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 10000

    def get_paginated_response(self, data):
        return Response(
            {
                "data": data,
                "count": self.page.paginator.count,
            }
        )


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = "page_size"
    max_page_size = 10000

    def get_paginated_response(self, data):
        return Response(
            {
                "data": data,
                "count": self.page.paginator.count,
            }
        )


class ConfigurationResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response(
            {
                "data": data,
                "count": self.page.paginator.count,
            }
        )
