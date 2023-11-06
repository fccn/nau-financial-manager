from rest_framework import serializers

from apps.organization.models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    """
    A serializer class for the `Organization` model.

    This serializer includes the `name`, `short_name` and `email` fields
    of the `Organization` model.
    """

    class Meta:
        model = Organization
        fields = ["name", "short_name", "email"]
