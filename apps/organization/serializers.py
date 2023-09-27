from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from apps.organization.models import Organization, OrganizationAddress, OrganizationContact
from apps.util.validators import validate_contact_value


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

    organization = OrganizationSerializer()

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
        validators = [validate_contact_value]
        fields = [
            "id",
            "organization",
            "contact_type",
            "contact_value",
            "description",
            "is_main",
        ]


class CompleteSerializer(serializers.Serializer):

    organization = OrganizationSerializer()
    addresses = serializers.ListField()
    contacts = serializers.ListField()

    def save(self, **kwargs):
        if not self.organization.is_valid():
            raise Exception(self.organization.errors)

        contact_list = [OrganizationContactSerializer(data=c) for c in self.contacts]
        for c in contact_list:
            if not c.is_valid():
                raise Exception(self.organization.errors)

        address_list = [OrganizationContactSerializer(data=c) for c in self.contacts]
        for c in address_list:
            if not c.is_valid():
                raise Exception(self.organization.errors)

        return super().save(**kwargs)
