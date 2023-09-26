from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.organization.models import Organization, OrganizationAddress, OrganizationContact
from apps.organization.serializers import (
    OrganizationAddressSerializer,
    OrganizationContactSerializer,
    OrganizationSerializer,
)
from apps.util.base_views import DetailDelete, DetailGet, DetailPut, GeneralGet, GeneralPost


class OrganizationGeneral(APIView, GeneralGet, GeneralPost):

    """

    For the post method, the required fields are name, short_name, slug e vat_number
    """

    model = Organization
    serializer = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    search_fields = (
        "name",
        "short_name",
        "slug",
        "vat_number",
        "iban",
    )

    ordering_fields = [
        "uuid",
        "name",
        "short_name",
        "slug",
        "vat_country",
        "vat_number",
        "iban",
    ]

    ordering = ["name", "slug", "vat_number", "iban"]


class OrganizationDetail(APIView, DetailGet, DetailDelete, DetailPut):

    """

    This view deals with a single register of Organization model
    For filtering a register, though the url as is necessary give the register slug
    """

    model = Organization
    serializer = OrganizationSerializer
    permission_classes = [IsAuthenticated]


class OrganizationAddressGeneral(APIView, GeneralGet, GeneralPost):

    """

    For the post method just the field organization is required
    """

    model = OrganizationAddress
    serializer = OrganizationAddressSerializer
    permission_classes = [IsAuthenticated]

    search_fields = (
        "address_type",
        "street",
        "postal_code",
    )

    ordering_fields = [
        "organization",
        "address_type",
        "street",
        "postal_code",
        "city",
        "district",
        "country",
    ]

    ordering = ["organization", "postal_code"]


class OrganizationAddressDetail(APIView, DetailGet, DetailDelete, DetailPut):

    """

    This view deals with a single register of OrganizationAddress model
    For filtering a register, though the url as is necessary give the register index number
    """

    model = OrganizationAddress
    serializer = OrganizationAddressSerializer
    permission_classes = [IsAuthenticated]

    prefetch_related_fields = ("organization",)


class OrganizationContactGeneral(APIView, GeneralGet, GeneralPost):

    """

    For the post method, the required fields are organization, contact_type, contact_value
    """

    model = OrganizationContact
    serializer = OrganizationContactSerializer
    permission_classes = [IsAuthenticated]

    search_fields = ("contact_value",)

    ordering_fields = [
        "organization",
        "contact_type",
        "contact_value",
        "description",
        "is_main",
    ]

    ordering = ["organization", "contact_value", "is_main"]


class OrganizationContactDetail(APIView, DetailGet, DetailDelete, DetailPut):

    """

    This view deals with a single register of OrganizationContact model
    For filtering a register, through the url is necessary give the register index number
    """

    model = OrganizationContact
    serializer = OrganizationContactSerializer
    permission_classes = [IsAuthenticated]

    prefetch_related_fields = ("organization",)
