from django.core.validators import MaxValueValidator, MinValueValidator
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from apps.billing.models import Transaction, TransactionItem
from apps.billing.tasks import send_transactions_to_processor_task
from apps.organization.models import Organization
from apps.shared_revenue.models import RevenueConfiguration


class TransactionItemSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    A serializer class for the `TransactionItem` model.

    This serializer includes the `transaction`, `description`, `quantity`, `vat_tax`, `unit_price_excl_vat`,
    `unit_price_incl_vat`, `organization_code`, `product_code`, `product_id` and `discount` fields of the `TransactionItem` model.
    """

    # Redefined the discount field because for some reason it isn't using the model default value.
    # So the solution was to define it again in the Serializer.
    discount = serializers.DecimalField(
        default=0.00,
        max_digits=3,
        decimal_places=2,
        validators=[MaxValueValidator(1), MinValueValidator(0)],
    )

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
            "organization_code",
            "product_id",
            "product_code",
            "discount",
        ]


class TransactionSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    A serializer class for the `Transaction` model.

    This serializer includes the `id`, `client_name`, `email`, `address_line_1`, `address_line_2,` `vat_identification_country`,
    `vat_identification_number`, `city`, `postal_code`, `state`, `country_code`, `total_amount_exclude_vat`, `total_amount_include_vat`, `payment_type`,
    `transaction_id`, `currency`, `transaction_date`, `transaction_type`, `document_id` and `transaction_items` fields of the `Transaction` model. The `transaction_items` field is a nested
    serializer that includes the `TransactionItem` model fields.
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
            "currency",
            "payment_type",
            "transaction_type",
            "transaction_date",
        ]


class TransactionItemSerializerWithoutTransaction(TransactionItemSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["transaction"]


class ProcessTransactionSerializer(CountryFieldMixin, serializers.ModelSerializer):
    """
    Serializer for processing transactions.
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

    items = serializers.ListField()

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
        validate_data: dict,
    ) -> tuple[Transaction, list[TransactionItem]]:
        items = validate_data.pop("items", [])
        transaction = Transaction.objects.create(**validate_data)
        items_as_instances: list[TransactionItem] = []
        serialized_items = []
        for item in items:
            item["transaction"] = transaction
            item = TransactionItem.objects.create(**item)
            items_as_instances.append(item)
            serialized_items.append(TransactionItemSerializer(item).data)

        validate_data["items"] = serialized_items
        return transaction, items_as_instances

    def create(self, validate_data):
        try:
            transaction, items = self._execute_billing_resources(validate_data=validate_data)
            for item in items:
                organization, created = Organization.objects.get_or_create(
                    short_name=item.organization_code,
                    defaults={"short_name": item.organization_code},
                )
                self._execute_shared_revenue_resources(
                    organization=organization,
                    product_id=item.product_id,
                )

            send_transactions_to_processor_task(transaction=transaction)

            return validate_data
        except Exception as e:
            raise e

    def to_representation(self, instance):
        return instance

    def validate(self, data):
        serializer_fields = set(self.fields.keys())
        data_fields = set(self.initial_data.keys())
        extra_fields = data_fields - serializer_fields
        if extra_fields:
            raise serializers.ValidationError(f"Extra fields: {', '.join(extra_fields)}")

        items = data.pop("items", [])
        transaction = TransactionSerializer(data=data)
        transaction.is_valid(raise_exception=True)
        serialized_items = []

        for item in items:
            item = TransactionItemSerializerWithoutTransaction(data=item)
            item.is_valid(raise_exception=True)
            serialized_items.append(item.data)

        transaction = transaction.data
        transaction["items"] = serialized_items

        return transaction
