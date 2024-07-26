from decimal import ROUND_HALF_UP, Decimal

from django.conf import settings
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from apps.billing.models import Transaction, TransactionItem
from apps.billing.tasks import create_and_async_send_transactions_to_processor_task
from apps.organization.models import Organization
from apps.shared_revenue.models import RevenueConfiguration


class TransactionItemSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    A serializer class for the `TransactionItem` model.
    """

    class Meta:
        model = TransactionItem
        fields = [
            "id",
            "transaction",
            "description",
            "quantity",
            "vat_tax",
            "unit_price_excl_vat",
            "unit_price_incl_vat",
            "discount_excl_tax",
            "discount_incl_tax",
            "organization_code",
            "product_id",
            "product_code",
        ]


class TransactionSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    A serializer class for the `Transaction` model.
    """

    class Meta:
        model = Transaction
        fields = [
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
            "total_discount_excl_tax",
            "total_discount_incl_tax",
            "currency",
            "payment_type",
            "transaction_type",
            "transaction_date",
        ]


class TransactionItemSerializerWithoutTransaction(TransactionItemSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["transaction"]


class TransactionItemSerializerForAPI(serializers.ModelSerializer):
    class Meta:
        model = TransactionItem
        fields = [
            "id",
            "description",
            "quantity",
            "unit_price_incl_vat",
            "discount_incl_tax",
            "organization_code",
            "product_id",
            "product_code",
        ]


class ProcessTransactionSerializerForAPI(CountryFieldMixin, serializers.ModelSerializer):
    """
    Serializer for processing transactions on API.
    This serializer is responsible for validating and processing transaction data. It includes methods for creating
    transactions, executing shared revenue resources, and converting transaction data to internal and external formats.
    Methods:
        _execute_shared_revenue_resources(organization: Organization, product_id: str): Checks if a revenue configuration
            exists for the given organization and product ID, and creates one if it doesn't exist.
        _execute_billing_resources(validate_data: dict): Creates a transaction and a transaction item from the given data.
        create(validate_data): Creates a transaction, a transaction item, and a revenue configuration from the given data.
        to_internal_value(data): Converts the given data to an internal format.
        to_representation(instance): Returns the given instance.
    """

    items = TransactionItemSerializerForAPI(many=True)

    class Meta:
        model = Transaction
        fields = [
            "items",
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
            "total_amount_include_vat",
            "total_discount_incl_tax",
            "currency",
            "payment_type",
            "transaction_date",
        ]

    def _execute_shared_revenue_resources(
        self,
        organization: Organization,
        product_id: str,
    ):
        try:
            revenue_configuration_exists = RevenueConfiguration(
                organization=organization,
                product_id=product_id,
            ).has_concurrent_revenue_configuration()
            if not revenue_configuration_exists:
                RevenueConfiguration.objects.create(**{"organization": organization, "product_id": product_id})
        except Exception:
            return True

    def _execute_billing_resources(
        self,
        data: dict,
    ) -> tuple[Transaction, list[TransactionItem]]:
        items = data.pop("items", [])
        transaction = Transaction.objects.create(**data)
        items_as_instances: list[TransactionItem] = []
        serialized_items = []
        for item in items:
            item["transaction"] = transaction
            item = TransactionItem.objects.create(**item)
            items_as_instances.append(item)
            serialized_items.append(TransactionItemSerializer(item).data)

        data["items"] = serialized_items
        return transaction, items_as_instances

    def create(self, validated_data):
        transaction, items = self._execute_billing_resources(data=validated_data)
        for item in items:
            organization, created = Organization.objects.get_or_create(
                short_name=item.organization_code,
                defaults={"short_name": item.organization_code},
            )
            self._execute_shared_revenue_resources(
                organization=organization,
                product_id=item.product_id,
            )

        create_and_async_send_transactions_to_processor_task(transaction=transaction)

        return validated_data

    def to_representation(self, instance):
        return instance

    def validate(self, data):
        additional_data = {
            "total_amount_exclude_vat": get_excl_tax(data.get("total_amount_include_vat")),
            "total_discount_excl_tax": get_excl_tax(data.get("total_discount_incl_tax")),
        }
        additional_data_fields = set(additional_data.keys())
        serializer_fields = set(self.fields.keys())
        initial_data_fields = set(self.initial_data.keys())
        extra_fields = initial_data_fields - serializer_fields - additional_data_fields
        if extra_fields:
            raise serializers.ValidationError(f"Extra fields: {', '.join(extra_fields)}")

        data = {**data, **additional_data}
        items_data = data.pop("items", [])
        transaction = TransactionSerializer(data=data)
        transaction.is_valid(raise_exception=True)
        serialized_items = []

        for item_data in items_data:
            item_data = {
                **item_data,
                **{
                    "unit_price_excl_vat": get_excl_tax(item_data.get("unit_price_incl_vat")),
                    "discount_excl_tax": get_excl_tax(item_data.get("discount_incl_tax")),
                    "vat_tax": settings.VAT_TAX_RATE,
                },
            }
            item = TransactionItemSerializerWithoutTransaction(data=item_data)
            item.is_valid(raise_exception=True)
            serialized_items.append(item.data)

        transaction = transaction.data
        transaction["items"] = serialized_items

        return transaction


def get_excl_tax(value_incl_vat_tax):
    """
    Calculate the value excluding vat tax from the including tax value.
    """
    return round(value_incl_vat_tax / (1 + Decimal(settings.VAT_TAX_RATE)))


def round(value: Decimal) -> Decimal:
    """
    Round 2 decimal cases.
    """
    return Decimal(value.quantize(Decimal(".01"), rounding=ROUND_HALF_UP))
