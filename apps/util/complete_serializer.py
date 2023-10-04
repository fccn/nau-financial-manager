from rest_framework import serializers

from apps.billing.serializers import ReceiptItemSerializer, ReceiptSerializer
from apps.organization.models import Organization
from apps.shared_revenue.models import RevenueConfiguration
from apps.shared_revenue.serializers import PartnershipLevelSerializer, RevenueConfigurationSerializer


class CompleteSerializer(serializers.Serializer):
    class Meta:
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
            "item",
        ]

    transaction_id = serializers.CharField(allow_blank=True)
    client_name = serializers.CharField(allow_blank=True)
    email = serializers.CharField(allow_blank=True)
    address_line_1 = serializers.CharField(allow_blank=True)
    address_line_2 = serializers.CharField(allow_blank=True)
    city = serializers.CharField(allow_blank=True)
    postal_code = serializers.CharField(allow_blank=True)
    state = serializers.CharField(allow_blank=True)
    country_code = serializers.CharField(allow_blank=True)
    vat_identification_number = serializers.CharField(allow_blank=True)
    vat_identification_country = serializers.CharField(allow_blank=True)
    total_amount_exclude_vat = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_amount_include_vat = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(allow_blank=True)
    item = serializers.JSONField()

    def __create_shared_revenue_resources(
        self,
        organization: Organization,
        course_id: str,
    ):
        partnership_level = PartnershipLevelSerializer(data=None).save()
        revenue_configuration = RevenueConfigurationSerializer(
            data={
                "organization": organization,
                "course_id": course_id,
                "partnership_level": partnership_level,
                "start_date": "",
                "end_date": "",
            }
        )
        if not revenue_configuration.is_valid():
            return revenue_configuration
        revenue_configuration = revenue_configuration.save()

    def __create_billing_resources(
        self,
        validade_data: dict,
    ):
        receipt_data = {k: v for k, v in validade_data.items() if k != "item"}
        receipt = ReceiptSerializer(data=receipt_data)
        if receipt.is_valid():
            receipt = receipt.save()

        receipt_item = validade_data["item"]
        receipt_item["receipt_id"] = receipt.uuid
        receipt_item = ReceiptItemSerializer(data=receipt_item)
        if receipt_item.is_valid():
            receipt_item = receipt_item.save()

        return ReceiptSerializer(receipt)

    def create(self, validade_data):
        try:
            organization, created = Organization.objects.get_or_create(
                short_name=validade_data["item"]["organization_code"],
                defaults={"short_name": validade_data["item"]["organization_code"]},
            )

            course_id: str = validade_data["item"]["course_id"]
            revenue_configuration: RevenueConfiguration = RevenueConfiguration.objects.filter(
                **{"course_id": course_id, "organization": organization}
            ).first()

            if revenue_configuration is None:
                self.__create_shared_revenue_resources(
                    organization=organization,
                    course_id=course_id,
                )

            return self.__create_billing_resources(validade_data=validade_data)
        except Exception as e:
            raise e
