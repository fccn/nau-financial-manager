from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.shared_revenue.models import RevenueConfiguration
from apps.shared_revenue.serializers import RevenueConfigurationSerializer
from apps.util.base_views import DetailDelete, DetailGet, DetailPut, GeneralGet, GeneralPost


class RevenueConfigurationGeneral(APIView, GeneralGet, GeneralPost):
    """
    List all RevenueConfiguration, or create a new one.
    """

    model = RevenueConfiguration
    serializer = RevenueConfigurationSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    )
    search_fields = ("product_code", "start_date", "end_date")
    ordering_fields = [
        "product_code",
        "start_date",
        "end_date",
    ]
    ordering = ["product_code", "start_date", "end_date"]


class RevenueConfigurationDetail(APIView, DetailDelete, DetailPut, DetailGet):
    """
    List single RevenueConfiguration, update or delete.
    """

    model = RevenueConfiguration
    serializer = RevenueConfigurationSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    prefetch_related_fields = "organization"
