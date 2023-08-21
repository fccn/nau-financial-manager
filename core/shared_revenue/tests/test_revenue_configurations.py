from django.db.utils import IntegrityError
from django.test import TestCase

from core.organization.factories import OrganizationFactory
from core.shared_revenue.factories import PartnershipLevelFactory, RevenueConfigurationFactory


class RevenueConfigurationTestCase(TestCase):
    def setUp(self):
        self.organization = OrganizationFactory()
        self.partnership_level = PartnershipLevelFactory()
        self.revenue_configuration = RevenueConfigurationFactory(
            organization=self.organization, partnership_level=self.partnership_level
        )

    def test_str_method(self):
        self.assertEqual(
            str(self.revenue_configuration),
            f"{self.organization} - {self.revenue_configuration.course_code} - {self.partnership_level}",
        )

    def test_organization_or_course_code_constraint(self):
        with self.assertRaises(IntegrityError):
            RevenueConfigurationFactory(organization=None, course_code=None)

    def test_organization_and_course_code_constraint(self):
        with self.assertRaises(IntegrityError):
            RevenueConfigurationFactory(organization=self.organization, course_code="ABC123")
