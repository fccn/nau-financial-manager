from datetime import datetime, timedelta
from typing import Callable, Iterable, Tuple

from django.core import paginator as pg
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from apps.util.constants import PER_PAGE


class ApiQuery:
    """
    A utility class for performing common API query operations.
    This class provides static methods for paginating query results and filtering querysets using filter backends.
    """

    @staticmethod
    def paginator(result_query, total_results, page):
        """
        Paginates a query result.
        """
        paginator = pg.Paginator(result_query, int(total_results))

        try:
            result_query = paginator.page(page)
        except pg.PageNotAnInteger:
            result_query = paginator.page(1)
        except pg.EmptyPage:
            result_query = paginator.page(paginator.num_pages)
        return result_query

    @staticmethod
    def filter_queryset(filter_backends, request, queryset, view):
        """
        Filters a queryset using filter backends.
        """
        for backend in list(filter_backends):
            queryset = backend().filter_queryset(request, queryset, view)

        return queryset


class Format:
    """
    A utility class for formatting data.

    This class provides static methods for formatting error messages, success responses, and dates.
    """

    @staticmethod
    def limit_string_size(string, tam):
        """
        Limits the size of a string.
        """
        if isinstance(string, str):
            return string[:tam]
        return string

    @staticmethod
    def format_error_limit_string(**kwargs):
        """
        Formats an error message.
        """
        error = {
            "error": [
                {
                    "code": kwargs["codeError"],
                    "title": Format.limit_string_size(kwargs["nomeErro"], 60),
                    "description": Format.limit_string_size(kwargs["descricaoErro"], 255),
                }
            ]
        }
        return error

    @staticmethod
    def format_success(**kwargs):
        """
        Formats a success response.
        """
        return {"code": kwargs["codeError"], "data": kwargs["data"]}

    @staticmethod
    def format_success_paginated(**kwargs):
        """
        Formats a paginated success response.
        """
        return {
            "code": kwargs["codeError"],
            "data": kwargs["data"],
            "recordCount": kwargs["recordCount"],
        }

    @staticmethod
    def format_date(timestamp):
        """
        Formats a timestamp as a date.
        """
        formated_date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
        formated_date = datetime.strptime(formated_date, "%Y-%m-%d")
        return formated_date

    @staticmethod
    def get_today():
        """
        Gets the current date as a timestamp.
        """
        formated_date = datetime.now() - timedelta(days=365)
        formated_date = formated_date.timestamp()
        return formated_date

    @staticmethod
    def get_yesterday():
        """
        Gets yesterday's date as a timestamp.
        """
        formated_date = datetime.now() - timedelta(days=1)
        formated_date = formated_date.timestamp()
        return formated_date


class CustomPageNumberPagination(PageNumberPagination):
    """
    A custom pagination class that extends the `PageNumberPagination` class.
    This class provides custom query parameters for pagination.
    """

    page_query_param = "page"
    page_size_query_param = "perPage"
    page_size = PER_PAGE


class BaseAPIView:
    """
    A base class for API views.
    """

    model: Model
    serializer: Callable
    permission_classes: Iterable
    select_related_fields: Tuple
    prefetch_related_fields: Tuple
    errors: dict
    custom_class_prefix_serializer: str
    custom_prefixes_serializers: list = ["basic"]

    @classmethod
    def get_object(cls, **kwargs):
        """
        Returns an object from the queryset based on the primary key.
        """
        queryset = cls.model.objects

        if hasattr(cls, "select_related_fields"):
            queryset = queryset.select_related(*cls.select_related_fields)

        if hasattr(cls, "prefetch_related_fields"):
            queryset = queryset.prefetch_related(*cls.prefetch_related_fields)

        return queryset.get(**kwargs)

    def get_queryset(self, _, **relations):
        """
        Returns a queryset filtered by the given relations.
        """
        return self.model.objects.filter(**relations)

    def get_context(self, request):
        """
        Returns a dictionary of context data for the view.
        """
        return {}

    def get_serializer(self, *args, **kwargs) -> serializers.ModelSerializer:
        """
        Returns the serializer instance for the view.
        """
        serializer_name = "serializer"

        self.custom_prefixes_serializers.append(self.custom_class_prefix_serializer)

        for prefix_serializer in self.custom_prefixes_serializers:
            expected_serializer_name = prefix_serializer + "_custom_serializer"

            if hasattr(self, expected_serializer_name):
                serializer_name = expected_serializer_name

        return getattr(self, serializer_name)(*args, **kwargs)


class GeneralGet(BaseAPIView):
    """
    Base class for General APIViews for the GET HTTP method
    """

    pagination_class = PageNumberPagination
    paginator = CustomPageNumberPagination()
    custom_class_prefix_serializer = "get"
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    )

    def get(self, request, **relations):
        queryset = self.get_queryset(request, **relations)

        if hasattr(self, "select_related_fields"):
            queryset = queryset.select_related(*self.select_related_fields)

        if hasattr(self, "prefetch_related_fields"):
            queryset = queryset.prefetch_related(*self.prefetch_related_fields)

        serializer = self.get_serializer

        queryset = ApiQuery.filter_queryset(self.filter_backends, self.request, queryset, self)

        page = self.paginator.paginate_queryset(queryset, request)
        is_paginated = request.query_params.get("page")
        if page is None or not is_paginated:
            content = Format.format_success(
                codeError=HTTP_200_OK,
                data=serializer(queryset, many=True, context=self.get_context(request)).data,
            )
        else:
            content = Format.format_success_paginated(
                codeError=HTTP_200_OK,
                data=serializer(page, many=True, context=self.get_context(request)).data,
                recordCount=queryset.count(),
            )

        return Response(
            content,
            content_type="application/json; charset=utf-8",
            status=HTTP_200_OK,
        )


class GeneralPost(BaseAPIView):
    """
    Base class for General APIViews for the POST HTTP method
    """

    can_bulk_create = False
    custom_class_prefix_serializer = "post"

    def post(self, request):
        if self.can_bulk_create and isinstance(request.data, list):
            serializer = self.serializer(data=request.data, many=True, context=self.get_context(request))
        else:
            serializer = self.serializer(data=request.data, context=self.get_context(request))

        if serializer.is_valid():
            serializer.save()

            return Response(
                Format.format_success(codeError=HTTP_201_CREATED, data=serializer.data),
                content_type="application/json; charset=utf-8",
                status=HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class DetailGet(BaseAPIView):
    """
    Base class for Detail APIViews for the GET HTTP method
    """

    custom_class_prefix_serializer = "get"

    def get(self, request, **kwargs):
        try:
            object_instance = self.get_object(**kwargs)

            serializer = self.serializer(object_instance, context=self.get_context(request))

            return Response(
                Format.format_success(codeError=HTTP_200_OK, data=serializer.data),
                content_type="application/json; charset=utf-8",
                status=HTTP_200_OK,
            )

        except ObjectDoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)


class DetailPut(BaseAPIView):
    """
    Base class for Detail APIViews for the PUT HTTP method
    """

    custom_class_prefix_serializer = "put"

    def put(self, request, **kwargs):
        try:
            object_instance = self.get_object(**kwargs)

            if hasattr(self, "put_is_valid"):
                if not self.put_is_valid(request, object_instance):
                    return Response(self.errors, status=HTTP_400_BAD_REQUEST)

            serializer = self.serializer(
                object_instance,
                data=request.data,
                context=self.get_context(request),
            )
            if serializer.is_valid():
                serializer.save()

                return Response(
                    Format.format_success(codeError=HTTP_200_OK, data=serializer.data),
                    content_type="application/json; charset=utf-8",
                    status=HTTP_200_OK,
                )

            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)


class DetailPatch(BaseAPIView):
    """
    Base class for Detail APIViews for the PATH HTTP method
    """

    custom_class_prefix_serializer = "patch"

    def patch(self, request, **kwargs):
        try:
            object_instance = self.get_object(**kwargs)
            serializer = self.serializer(
                object_instance,
                data=request.data,
                partial=True,
                context=self.get_context(request),
            )
            if serializer.is_valid():
                serializer.save()

                return Response(
                    Format.format_success(codeError=HTTP_200_OK, data=serializer.data),
                    content_type="application/json; charset=utf-8",
                    status=HTTP_200_OK,
                )

            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)


class DetailDelete(BaseAPIView):
    """
    Base class for Detail APIViews for the DELETE HTTP method
    """

    custom_class_prefix_serializer = "delete"

    def delete(self, request, **kwargs):
        try:
            object_instance = self.get_object(**kwargs)

            if hasattr(self, "delete_is_valid"):
                if not self.delete_is_valid(request, object_instance):
                    return Response(self.errors, status=HTTP_400_BAD_REQUEST)

            object_instance.delete()

            return Response(status=HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
