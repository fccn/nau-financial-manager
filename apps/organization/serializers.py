from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from apps.organization.models import Organization, OrganizationAddress, OrganizationContact


class OrganizationSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    A serializer class for the `Organization` model.

    This serializer includes the `uuid`, `name`, `short_name`, `slug`, `vat_country`, `vat_number`, and `iban` fields
    of the `Organization` model.
    """

    class Meta:
        model = Organization
        fields = [
            "uuid",
            "name",
            "short_name",
            "slug",
            "vat_country",
            "vat_number",
            "iban",
        ]


class OrganizationAddressSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    A serializer class for the `OrganizationAddress` model.

    This serializer includes the `id`, `organization`, `address_type`, `street`, `postal_code`, `city`, `district`,
    and `country` fields of the `OrganizationAddress` model.
    """

    class Meta:
        model = OrganizationAddress
        fields = [
            "id",
            "organization",
            "address_type",
            "street",
            "postal_code",
            "city",
            "district",
            "country",
        ]


class OrganizationContactSerializer(serializers.ModelSerializer):
    """
    A serializer class for the `OrganizationContact` model.

    This serializer includes the `id`, `organization`, `contact_type`, `contact_value`, `description`, and `is_main`
    fields of the `OrganizationContact` model.
    """

    class Meta:
        model = OrganizationContact
        fields = [
            "id",
            "organization",
            "contact_type",
            "contact_value",
            "description",
            "is_main",
        ]
