from copy import deepcopy

from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from apps.billing.models import Receipt, ReceiptItem
from apps.organization.models import Organization
from apps.shared_revenue.models import PartnershipLevel, RevenueConfiguration


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
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    item = serializers.JSONField(required=False)
    transaction_id = serializers.CharField(required=False)

    class Meta:
        model = Receipt
        fields = "__all__"

    def __create_shared_revenue_resources(
        self,
        organization: Organization,
        product_id: str,
    ):
        partnership_level, created = PartnershipLevel.objects.get_or_create(percentage=0.70)
        RevenueConfiguration.objects.create(
            **{"organization": organization, "product_id": product_id, "partnership_level": partnership_level}
        )

    def __create_billing_resources(
        self,
        validate_data: dict,
    ):
        receipt_data = {k: v for k, v in validate_data.items() if k != "item"}
        receipt = ReceiptSerializer(data=receipt_data)
        if receipt.is_valid():
            receipt = Receipt.objects.create(**receipt.data)

        receipt_item_data = deepcopy(validate_data["item"])
        receipt_item_data["receipt"] = receipt
        ReceiptItem.objects.create(**receipt_item_data)

        return receipt

    def __check_revenue_configuration_exists(
        self,
        organization: Organization,
        product_id: str,
    ):
        same_revenue_configuration: RevenueConfiguration = RevenueConfiguration.objects.filter(
            **{
                "organization": organization,
                "product_id": product_id,
            }
        ).first()

        return same_revenue_configuration is not None

    def create(self, validate_data):
        try:
            receipt: Receipt = self.__create_billing_resources(validate_data=validate_data)

            organization, created = Organization.objects.get_or_create(
                short_name=validate_data["item"]["organization_code"],
                defaults={"short_name": validate_data["item"]["organization_code"]},
            )

            product_id: str = validate_data["item"]["course_id"]
            revenue_configuration_exists: bool = self.__check_revenue_configuration_exists(
                organization=organization,
                product_id=product_id,
            )

            if not revenue_configuration_exists:
                self.__create_shared_revenue_resources(
                    organization=organization,
                    product_id=product_id,
                )

            return receipt
        except Exception as e:
            raise e
