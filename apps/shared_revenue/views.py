from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.shared_revenue.models import PartnershipLevel, RevenueConfiguration, ShareExecution
from apps.shared_revenue.serializers import (
    PartnershipLevelSerializer,
    RevenueConfigurationSerializer,
    ShareExecutionSerializer,
)
from apps.util.base_views import DetailDelete, DetailGet, DetailPut, GeneralGet, GeneralPost


class PartnershipLevelGeneral(APIView, GeneralGet, GeneralPost):
    """
    List all PartnershipLevel, or create a new one.
    """

    model = PartnershipLevel
    serializer = PartnershipLevelSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    )
    search_fields = ("name", "description", "percentage")
    ordering_fields = [
        "name",
        "description",
        "percentage",
    ]
    ordering = ["name", "description", "percentage"]


class PartnershipLevelDetail(APIView, DetailDelete, DetailPut, DetailGet):
    """
    List single PartnershipLevel, update or delete.
    """

    model = PartnershipLevel
    serializer = PartnershipLevelSerializer
    permission_classes = [
        IsAuthenticated,
    ]


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
    search_fields = ("course_code", "start_date", "end_date")
    ordering_fields = [
        "course_code",
        "start_date",
        "end_date",
    ]
    ordering = ["course_code", "start_date", "end_date"]


class RevenueConfigurationDetail(APIView, DetailDelete, DetailPut, DetailGet):
    """
    List single RevenueConfiguration, update or delete.
    """

    model = RevenueConfiguration
    serializer = RevenueConfigurationSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    prefetch_related_fields = ("organization", "partnership_level")


class ShareExecutionGeneral(APIView, GeneralGet, GeneralPost):
    """
    List all ShareExecution, or create a new one.
    """

    model = ShareExecution
    serializer = ShareExecutionSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    )
    search_fields = ("organization", "percentage", "executed", "receipt")
    ordering_fields = ["organization", "percentage", "executed", "receipt"]
    ordering = ["course_code", "start_date", "end_date"]


class ShareExecutionDetail(APIView, DetailDelete, DetailPut, DetailGet):
    """
    List single ShareExecution, update or delete.
    """

    model = ShareExecution
    serializer = ShareExecutionSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    prefetch_related_fields = ("organization",)
