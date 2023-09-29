from rest_framework import serializers

from apps.billing.models import Receipt, ReceiptItem
from apps.organization.models import Organization


class ReceiptItemSerializer(serializers.ModelSerializer):
    """
    A serializer class for the `ReceiptItem` model.

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
            "course_code",
            "course_id",
        ]


class ReceiptSerializer(serializers.ModelSerializer):
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
            "item",
        ]

    # transaction_id = serializers.CharField(allow_blank=True)
    # client_name = serializers.CharField(allow_blank=True)
    # email = serializers.CharField(allow_blank=True)
    # address_line_1 = serializers.CharField(allow_blank=True)
    # address_line_2 = serializers.CharField(allow_blank=True)
    # city = serializers.CharField(allow_blank=True)
    # postal_code = serializers.CharField(allow_blank=True)
    # state = serializers.CharField(allow_blank=True)
    # country_code = serializers.CharField(allow_blank=True)
    # vat_identification_number = serializers.CharField(allow_blank=True)
    # vat_identification_country = serializers.CharField(allow_blank=True)
    # total_amount_exclude_vat = serializers.DecimalField(max_digits=10, decimal_places=2)
    # total_amount_include_vat = serializers.DecimalField(max_digits=10, decimal_places=2)
    # currency = serializers.CharField(allow_blank=True)
    item = serializers.JSONField()

    def create(self, **kwargs):
        try:

            obj, created = Organization.objects.get_or_create(
                short_name=self.data["item"]["organization_code"],
                defaults={"short_name": self.data["item"]["organization_code"]},
            )

            receipt_data = {k: v for k, v in self.data.items() if k != "item"}
            receipt: Receipt = Receipt.objects.create(**receipt_data)

            receipt_item = self.data["item"]
            receipt_item["receipt_id"] = receipt.uuid
            ReceiptItem.objects.create(**receipt_item)

            return ReceiptSerializer(receipt)
        except Exception as e:
            raise e
