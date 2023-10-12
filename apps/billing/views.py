from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.billing.models import Receipt
from apps.billing.serializers import ReceiptSerializer, TransactionSerializer
from apps.util.base_views import DetailDelete, DetailGet, DetailPut, GeneralGet, GeneralPost


class ReceiptsGeneral(APIView, GeneralGet, GeneralPost):
    """
    List all Receipts, or create a new one.
    """

    model = Receipt
    serializer = ReceiptSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    )
    search_fields = ("email", "name")
    ordering_fields = [
        "name",
        "email",
        "organization",
    ]
    ordering = ["name", "email", "organization"]


class ReceiptsDetail(APIView, DetailDelete, DetailPut, DetailGet):
    """
    List single Receitps, update or delete.
    """

    model = Receipt
    serializer = ReceiptSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    prefetch_related_fields = ("organization",)


class ProcessTransaction(APIView, GeneralPost):
    authentication_classes = [TokenAuthentication]
    serializer = TransactionSerializer
    permission_classes = [IsAuthenticated]
