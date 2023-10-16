from copy import deepcopy

from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from apps.billing.models import Receipt, ReceiptItem
from apps.organization.models import Organization
from apps.shared_revenue.models import RevenueConfiguration


class ReceiptItemSerializer(serializers.ModelSerializer):
    """
    A serializer class for the `ReceiptItem` model.

    This serializer includes the `receipt`, `description`, `quantity`, `vat_tax`, `amount_exclude_vat`,
    `amount_include_vat`, `organization_code`, `course_code`, and `course_id` fields of the `ReceiptItem` model.
    """

    class Meta:
        model = ReceiptItem
        fields = [
            "id",
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

    This serializer includes the `id`, `client_name`, `email`, `address_line_1`, `address_line_2,` `vat_identification_country`,
    `vat_identification_number`, `city`, `postal_code`, `state`, `country_code`, `total_amount_exclude_vat`, `total_amount_include_vat`, `payment_type`,
    `transaction_id`, `currency` and `receipt_items` fields of the `Receipt` model. The `receipt_items` field is a nested
    serializer that includes the `ReceiptItem` model fields.
    """

    class Meta:
        model = Receipt
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    item = ReceiptItemSerializer()

    class Meta:
        model = Receipt
        fields = [
            "item",
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
            "payment_type",
        ]

    def _execute_shared_revenue_resources(
        self,
        organization: Organization,
        product_id: str,
    ):
        revenue_configuration_exists: bool = self._has_concurrent_revenue_configuration(
            organization=organization,
            product_id=product_id,
        )
        if not revenue_configuration_exists:
            RevenueConfiguration.objects.create(**{"organization": organization, "product_id": product_id})

    def _execute_billing_resources(
        self,
        validate_data: dict,
    ):
        receipt_data = {k: v for k, v in validate_data.items() if k != "item"}
        receipt = Receipt.objects.create(**receipt_data)

        receipt_item_data = deepcopy(validate_data["item"])
        receipt_item_data["receipt"] = receipt
        item = ReceiptItem.objects.create(**receipt_item_data)

        return receipt, item

    def _has_concurrent_revenue_configuration(
        self,
        organization: Organization,
        product_id: str,
    ):
        try:
            return RevenueConfiguration(
                organization=organization,
                product_id=product_id,
            ).has_concurrent_revenue_configuration()
        except Exception:
            return True

    def create(self, validate_data):
        try:
            organization, created = Organization.objects.get_or_create(
                short_name=validate_data["item"]["organization_code"],
                defaults={"short_name": validate_data["item"]["organization_code"]},
            )
            self._execute_shared_revenue_resources(
                organization=organization,
                product_id=validate_data["item"]["course_id"],
            )
            return validate_data
        except Exception as e:
            raise e

    def to_internal_value(self, data):
        receipt, item = self._execute_billing_resources(validate_data=data)
        data = ReceiptSerializer(receipt).data
        data["item"] = ReceiptItemSerializer(item).data
        return data

    def to_representation(self, instance):
        return instance
