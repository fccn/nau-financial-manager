from rest_framework import serializers

from apps.billing.serializers import TransactionSerializer
from apps.organization.serializers import OrganizationSerializer
from apps.shared_revenue.models import RevenueConfiguration, ShareExecution


class RevenueConfigurationSerializer(serializers.ModelSerializer):
    """
    A serializer class for the `RevenueConfiguration` model.

    This serializer includes the `id`, `organization`, `course_code`, `partner_percentage`, `start_date`, and `end_date`
    fields of the `RevenueConfiguration` model.
    """

    organization = OrganizationSerializer()

    class Meta:
        model = RevenueConfiguration
        fields = [
            "id",
            "organization",
            "product_id",
            "partner_percentage",
            "start_date",
            "end_date",
        ]


class ShareExecutionSerializer(serializers.ModelSerializer):
    """
    A serializer class for the `ShareExecution` model.

    This serializer includes the `id`, `organization`, `revenue_configuration`, `percentage`, `value`, `transaction`,
    `executed`, `response_payload`, and `transaction_details` fields of the `ShareExecution` model. The `transaction_details`
    field is a nested serializer that includes the `Transaction` model fields.
    """

    organization = OrganizationSerializer()
    revenue_configuration = RevenueConfigurationSerializer()
    transaction_details = TransactionSerializer(source="transaction")

    class Meta:
        model = ShareExecution
        fields = [
            "id",
            "organization",
            "revenue_configuration",
            "percentage",
            "value",
            "transaction",
            "executed",
            "response_payload",
            "transaction_details",
        ]
