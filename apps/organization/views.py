from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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

    def post(self, request, *args, **kwargs):

        try:
            organization: OrganizationSerializer = OrganizationSerializer(data=request.data["organization"])

            if not organization.is_valid():
                return Response(organization.errors, status=403)

            o = organization.save()

            for c in request.data["contacts"]:
                c["organization"] = OrganizationSerializer(o).data["uuid"]

            contacts: list[OrganizationContactSerializer] = [
                OrganizationContactSerializer(data=c) for c in request.data["contacts"]
            ]
            for c in contacts:
                if not c.is_valid():
                    return Response(
                        {
                            "contacts_errors": c.errors,
                            "organization": OrganizationSerializer(o).data,
                        },
                        status=403,
                    )

            for a in request.data["addresses"]:
                a["organization"] = OrganizationSerializer(o).data["uuid"]

            addresses: list[OrganizationAddressSerializer] = [
                OrganizationAddressSerializer(data=a) for a in request.data["addresses"]
            ]
            for a in addresses:
                if not a.is_valid():
                    return Response(
                        {
                            "address_errors": a.errors,
                            "organization": OrganizationSerializer(o).data,
                        },
                        status=403,
                    )

            __contacts = []
            for c in contacts:
                __c = c.save()
                __contacts.append(__c)

            __addresses = []
            for a in addresses:
                __a = a.save()
                __addresses.append(__a)

            response = {
                "organization": organization.data,
                "contacts": [OrganizationContactSerializer(c).data for c in __contacts],
                "addresses": [OrganizationAddressSerializer(a).data for a in __addresses],
            }
            return Response(response)
        except Exception as e:
            return Response(str(e))
