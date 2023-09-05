from django.test import TestCase

from apps.organization.factories import OrganizationAddressFactory, OrganizationContactFactory, OrganizationFactory
from apps.organization.models import OrganizationAddress, OrganizationContact


class OrganizationTest(TestCase):
    def test_organization_str(self):
        organization = OrganizationFactory()
        self.assertEqual(str(organization), organization.name)

    def test_organization_uuid_primary_key(self):
        organization = OrganizationFactory()
        self.assertIsNotNone(organization.uuid)

    def test_organization_vat_country_default(self):
        organization = OrganizationFactory()
        self.assertEqual(organization.vat_country, "PT")


class OrganizationAddressTest(TestCase):
    def test_organization_address_str(self):
        organization_address = OrganizationAddressFactory()
        expected_str = f"{organization_address.organization.name} - {organization_address.address_type}"
        self.assertEqual(str(organization_address), expected_str)

    def test_organization_address_verbose_name_plural(self):
        self.assertEqual(str(OrganizationAddress._meta.verbose_name_plural), "Organizations addresses")


class OrganizationContactTest(TestCase):
    def test_organization_contact_str(self):
        organization_contact = OrganizationContactFactory()
        expected_str = f"{organization_contact.organization.name} - {organization_contact.contact_type}"
        self.assertEqual(str(organization_contact), expected_str)

    def test_organization_contact_verbose_name_plural(self):
        self.assertEqual(str(OrganizationContact._meta.verbose_name_plural), "Organizations contacts")

    def test_organization_has_only_one_main_contact(self):
        organization_contact = OrganizationContactFactory(is_main=True)
        with self.assertRaises(Exception):
            OrganizationContactFactory(
                organization=organization_contact.organization,
                contact_type=organization_contact.contact_type,
                is_main=True,
            )

    def test_organization_contact_description_blank(self):
        organization_contact = OrganizationContactFactory(description="")
        self.assertIsNone(organization_contact.description)
