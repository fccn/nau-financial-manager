from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.organization.models import Organization
from apps.organization.serializers import OrganizationSerializer
from apps.util.base_views import DetailDelete, DetailGet, DetailPut, GeneralGet, GeneralPost


class OrganizationGeneral(APIView, GeneralGet, GeneralPost):
    """
    For the post method, the required fields are name, short_name, and email
    """

    model = Organization
    serializer = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    search_fields = (
        "name",
        "short_name",
        "email",
    )

    ordering_fields = ["uuid", "name", "short_name", "email"]

    ordering = ["name", "short_name"]


class OrganizationDetail(APIView, DetailGet, DetailDelete, DetailPut):
    """
    This view deals with a single register of Organization model
    For filtering a register, though the url as is necessary give the register slug
    """

    model = Organization
    serializer = OrganizationSerializer
    permission_classes = [IsAuthenticated]
