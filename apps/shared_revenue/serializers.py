from rest_framework import serializers

from apps.organization.serializers import OrganizationSerializer
from apps.shared_revenue.models import RevenueConfiguration


class RevenueConfigurationSerializer(serializers.ModelSerializer):
    """
    A serializer class for the `RevenueConfiguration` model.

    This serializer includes the `id`, `organization`, `product_code`, `partner_percentage`, `start_date`, and `end_date`
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
