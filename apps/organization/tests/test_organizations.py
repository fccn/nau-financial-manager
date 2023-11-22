import factory
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.organization.factories import OrganizationFactory
from apps.organization.models import Organization


class OrganizationModelTest(TestCase):
    def setUp(self):
        """
        Set up the test case by creating a client, endpoint, transaction, transaction item, and payload.
        Also create a new user and generate a token for that user.
        """
        self.client = APIClient()
        self.endpoint = "/api/organization/organizations"

        self.organization = factory.build(dict, FACTORY_CLASS=OrganizationFactory)
        self.payload = self.organization
        OrganizationFactory.create()

        # Create a new user and generate a token for that user
        self.user = get_user_model().objects.create_user(username="testuser", password="testpass")
        self.token = Token.objects.create(user=self.user)

    def test_name_label(self):
        organization = Organization.objects.get(id=1)
        field_label = organization._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "Name")

    def test_short_name_label(self):
        organization = Organization.objects.get(id=1)
        field_label = organization._meta.get_field("short_name").verbose_name
        self.assertEquals(field_label, "Short Name")

    def test_email_label(self):
        organization = Organization.objects.get(id=1)
        field_label = organization._meta.get_field("email").verbose_name
        self.assertEquals(field_label, "Email")

    def test_name_max_length(self):
        organization = Organization.objects.get(id=1)
        max_length = organization._meta.get_field("name").max_length
        self.assertEquals(max_length, 255)

    def test_object_name_is_name(self):
        organization = Organization.objects.get(id=1)
        expected_object_name = f"{organization.name}"
        self.assertEquals(expected_object_name, str(organization))
