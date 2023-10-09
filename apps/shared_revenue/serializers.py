from rest_framework import serializers

from apps.billing.serializers import ReceiptSerializer
from apps.organization.serializers import OrganizationSerializer
from apps.shared_revenue.models import PartnershipLevel, RevenueConfiguration, ShareExecution


class PartnershipLevelSerializer(serializers.ModelSerializer):
    """
    A serializer class for the `PartnershipLevel` model.

    This serializer includes the `id`, `name`, `description`, and `percentage` fields of the `PartnershipLevel` model.
    """

    class Meta:
        model = PartnershipLevel
        fields = [
            "id",
            "name",
            "description",
            "percentage",
        ]


class RevenueConfigurationSerializer(serializers.ModelSerializer):
    """
    A serializer class for the `RevenueConfiguration` model.

    This serializer includes the `id`, `organization`, `course_code`, `partnership_level`, `start_date`, and `end_date`
    fields of the `RevenueConfiguration` model.
    """

    organization = OrganizationSerializer()

    class Meta:
        model = RevenueConfiguration
        fields = [
            "id",
            "organization",
            "product_id",
            "partnership_level",
            "start_date",
            "end_date",
        ]


class ShareExecutionSerializer(serializers.ModelSerializer):
    """
    A serializer class for the `ShareExecution` model.

    This serializer includes the `id`, `organization`, `revenue_configuration`, `percentage`, `value`, `receipt`,
    `executed`, `response_payload`, and `receipt_details` fields of the `ShareExecution` model. The `receipt_details`
    field is a nested serializer that includes the `Receipt` model fields.
    """

    organization = OrganizationSerializer()
    revenue_configuration = RevenueConfigurationSerializer()
    receipt_details = ReceiptSerializer(source="receipt")

    class Meta:
        model = ShareExecution
        fields = [
            "id",
            "organization",
            "revenue_configuration",
            "percentage",
            "value",
            "receipt",
            "executed",
            "response_payload",
            "receipt_details",
        ]
