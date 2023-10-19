from copy import deepcopy

from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from apps.billing.models import Transaction, TransactionItem
from apps.organization.models import Organization
from apps.shared_revenue.models import RevenueConfiguration


class TransactionItemSerializer(serializers.ModelSerializer):
    """
    A serializer class for the `TransactionItem` model.

    This serializer includes the `transaction`, `description`, `quantity`, `vat_tax`, `amount_exclude_vat`,
    `amount_include_vat`, `organization`, `product_code`, and `product_id` fields of the `TransactionItem` model.
    """

    class Meta:
        model = TransactionItem
        fields = [
            "id",
            "transaction",
            "description",
            "quantity",
            "vat_tax",
            "amount_exclude_vat",
            "amount_include_vat",
            "organization",
            "product_id",
            "product_code",
        ]


class TransactionSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    A serializer class for the `Transaction` model.

    This serializer includes the `id`, `client_name`, `email`, `address_line_1`, `address_line_2,` `vat_identification_country`,
    `vat_identification_number`, `city`, `postal_code`, `state`, `country_code`, `total_amount_exclude_vat`, `total_amount_include_vat`, `payment_type`,
    `transaction_id`, `currency`, `transaction_date`, `transaction_type` and `transaction_items` fields of the `Transaction` model. The `transaction_items` field is a nested
    serializer that includes the `TransactionItem` model fields.
    """

    class Meta:
        model = Transaction
        fields = "__all__"


class ProcessTransactionSerializer(serializers.ModelSerializer):
    item = TransactionItemSerializer()

    class Meta:
        model = Transaction
        fields = [
            "item",
            "transaction_id",
            "transaction_type",
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
            "transaction_date",
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
        transaction_data = {k: v for k, v in validate_data.items() if k != "item"}
        transaction = Transaction.objects.create(**transaction_data)

        transaction_item_data = deepcopy(validate_data["item"])
        transaction_item_data["transaction"] = transaction
        item = TransactionItem.objects.create(**transaction_item_data)

        return transaction, item

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
                short_name=validate_data["item"]["organization"],
                defaults={"short_name": validate_data["item"]["organization"]},
            )
            self._execute_shared_revenue_resources(
                organization=organization,
                product_id=validate_data["item"]["product_id"],
            )
            return validate_data
        except Exception as e:
            raise e

    def to_internal_value(self, data):
        transaction, item = self._execute_billing_resources(validate_data=data)
        data = TransactionSerializer(transaction).data
        data["item"] = TransactionItemSerializer(item).data
        return data

    def to_representation(self, instance):
        return instance
