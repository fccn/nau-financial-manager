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
        Set up common test variables.
        """
        self.organization_factored = OrganizationFactory.create(name="Test Organization")
        self.organization = Organization.objects.get(id=self.organization_factored.id)

    def test_name_label(self):
        """
        Test the label of the name field.
        """
        field_label = self.organization._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "Name")

    def test_short_name_label(self):
        """
        Test the label of the short name field.
        """
        field_label = self.organization._meta.get_field("short_name").verbose_name
        self.assertEqual(field_label, "Short Name")

    def test_email_label(self):
        """
        Test the label of the email field.
        """
        field_label = self.organization._meta.get_field("email").verbose_name
        self.assertEqual(field_label, "Email")

    def test_name_max_length(self):
        """
        Test the maximum length of the name field.
        """
        max_length = self.organization._meta.get_field("name").max_length
        self.assertEqual(max_length, 255)

    def test_object_name_is_name(self):
        """
        Test that the string representation of the organization is its name.
        """
        expected_object_name = f"{self.organization.name}"
        self.assertEqual(expected_object_name, str(self.organization))

    def test_create_organization(self):
        """
        Test creating a new organization.
        """
        organization = OrganizationFactory(name="New Organization")
        self.assertEqual(Organization.objects.get(id=organization.id).name, "New Organization")

    def test_retrieve_organization(self):
        """
        Test retrieving an existing organization.
        """
        organization = Organization.objects.get(id=self.organization.id)
        self.assertEqual(organization.name, "Test Organization")

    def test_update_organization(self):
        """
        Test updating the name of an existing organization.
        """
        self.organization.name = "Updated Organization"
        self.organization.save()
        self.assertEqual(Organization.objects.get(id=self.organization.id).name, "Updated Organization")

    def test_delete_organization(self):
        """
        Test deleting an existing organization.
        """
        organization_id = self.organization.id
        self.organization.delete()
        with self.assertRaises(Organization.DoesNotExist):
            Organization.objects.get(id=organization_id)


class OrganizationAPITest(TestCase):
    """
    Test case for the organization API.
    """

    def setUp(self):
        """
        Set up common test variables.
        """
        self.client = APIClient()
        self.endpoint = "/api/organization/organizations/"

        self.organization_dict = factory.build(dict, FACTORY_CLASS=OrganizationFactory)
        self.payload = self.organization_dict
        self.organization = OrganizationFactory.create(**self.organization_dict)

        # Create a new user and generate a token for that user
        self.user = get_user_model().objects.create_user(username="testuser", password="testpass")
        self.token = Token.objects.create(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_organization(self):
        """
        Test retrieving an organization.
        """
        response = self.client.get(f"{self.endpoint}{self.organization.short_name}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["name"], self.organization.name)

    def test_create_organization(self):
        """
        Test creating a new organization.
        """
        data = self.payload
        data["name"] = "New Organization Builder"
        data["short_name"] = "neworgbuilder"
        response = self.client.post(self.endpoint, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["data"]["name"], data["name"])

    def test_update_organization(self):
        """
        Test updating an organization.
        """
        data = {"name": "Updated Organization"}
        response = self.client.put(f"{self.endpoint}{self.organization.short_name}/", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["name"], data["name"])

    def test_delete_organization(self):
        """
        Test deleting an organization.
        """
        response = self.client.delete(
            f"{self.endpoint}{self.organization.short_name}/",
        )
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Organization.DoesNotExist):
            Organization.objects.get(short_name=self.organization.short_name)
