from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.organization.models import Organization, OrganizationAddress, OrganizationContact
from apps.organization.serializers import (
    CompleteSerializer,
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

    ordering = ordering_fields


class OrganizationDetail(APIView, DetailGet, DetailDelete, DetailPut):

    """

    An organization is filtered by the slug field, who is passed through the url
    """

    model = Organization
    serializer = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    ordering_fields = [
        "uuid",
        "name",
        "short_name",
        "slug",
        "vat_country",
        "vat_number",
        "iban",
    ]

    ordering = ordering_fields


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

    ordering = ordering_fields


class OrganizationAddressDetail(APIView, DetailGet, DetailDelete, DetailPut):
    model = OrganizationAddress
    serializer = OrganizationAddressSerializer
    permission_classes = [IsAuthenticated]

    ordering_fields = [
        "organization",
        "address_type",
        "street",
        "postal_code",
        "city",
        "district",
        "country",
    ]

    ordering = ordering_fields
    prefetch_related_fields = ("organization",)


class OrganizationContactGeneral(APIView, GeneralGet, GeneralPost):

    """

    For the post method, the required fields are organization, contact_type, contact_value
    """

    model = OrganizationContact
    serializer = OrganizationContactSerializer
    permission_classes = [IsAuthenticated]

    search_fields = "contact_value"

    ordering_fields = [
        "organization",
        "contact_type",
        "contact_value",
        "description",
        "is_main",
    ]

    ordering = ordering_fields


class OrganizationContactDetail(APIView, DetailGet, DetailDelete, DetailPut):
    model = OrganizationContact
    serializer = OrganizationContactSerializer
    permission_classes = [IsAuthenticated]

    ordering_fields = [
        "organization",
        "contact_type",
        "contact_value",
        "description",
        "is_main",
    ]

    ordering = ordering_fields
    prefetch_related_fields = ("organization",)


class CompleteOrganizationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        data_from_request = request.data
        data = CompleteSerializer(data=data_from_request)
        if not data.is_valid():
            return Response(data.errors)
        return Response(data.data)
