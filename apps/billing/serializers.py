from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from apps.billing.models import Receipt, ReceiptItem


class ReceiptItemSerializer(serializers.ModelSerializer):
    """
    A serializer class for the `ReceiptItem` model.

    This serializer includes the `id`, `receipt`, `description`, `quantity`, `vat_tax`, `amount_exclude_vat`,
    `amount_include_vat`, `organization_code`, `course_code`, and `course_id` fields of the `ReceiptItem` model.
    """

    class Meta:
        model = ReceiptItem
        fields = [
            "receipt",
            "description",
            "quantity",
            "vat_tax",
            "amount_exclude_vat",
            "amount_include_vat",
            "organization_code",
            "course_id",
            "course_code",
        ]


class ReceiptSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    A serializer class for the `Receipt` model.

    This serializer includes the `id`, `name`, `email`, `address`, `vat_identification_country`,
    `vat_identification_number`, `total_amount_exclude_vat`, `total_amount_include_vat`, `receipt_link`,
    `receipt_document_id`, and `receipt_items` fields of the `Receipt` model. The `receipt_items` field is a nested
    serializer that includes the `ReceiptItem` model fields.
    """

    class Meta:
        model = Receipt
        fields = [
            "uuid",
            "transaction_id",
            "client_name",
            "email",
            "address_line_1",
            "address_line_2",
            "city",
            "postal_code",
            "state",
            "country_code",
            "vat_identification_number",
            "vat_identification_country",
            "total_amount_exclude_vat",
            "total_amount_include_vat",
            "currency",
        ]
