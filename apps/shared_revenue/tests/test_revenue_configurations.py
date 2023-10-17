from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from apps.organization.factories import OrganizationFactory
from apps.shared_revenue.factories import RevenueConfigurationFactory


class RevenueConfigurationTestCase(TestCase):
    def setUp(self):
        self.organization = OrganizationFactory()
        self.revenue_configuration = RevenueConfigurationFactory(organization=self.organization)

    def test_str_method(self):
        """
        Test the `__str__` method of the `RevenueConfiguration` model.
        """
        self.assertEqual(
            str(self.revenue_configuration), f"{self.organization} - {self.revenue_configuration.course_code}"
        )

    def test_organization_or_course_code_without_course_or_organization(self):
        """
        Test that attempting to create a `RevenueConfiguration` instance without an `organization`
        or `course_code` raises an `IntegrityError`.
        """
        with self.assertRaises(IntegrityError):
            RevenueConfigurationFactory(organization=None, course_code=None)

    def test_organization_and_course_code_can_not_be_both_filled(self):
        """
        Test that attempting to create a `RevenueConfiguration` instance with both an `organization`
        and a `course_code` raises an `IntegrityError`.
        """
        with self.assertRaises(IntegrityError):
            RevenueConfigurationFactory(organization=self.organization, course_code="ABC123")

    def test_organization_null(self):
        """
        Test that attempting to create a `RevenueConfiguration` instance with a null `organization`
        and null `course_code` raises a `ValidationError`.
        """
        with self.assertRaises(ValidationError):
            RevenueConfigurationFactory(course_code="ABC123")

    def test_course_code_null(self):
        """
        Test that attempting to create a `RevenueConfiguration` instance with a null `course_code`
        and null `organization` raises a `ValidationError`.
        """
        with self.assertRaises(ValidationError):
            RevenueConfigurationFactory(organization=self.organization)

    def test_start_date_is_now(self):
        """
        Test that the `start_date` field is automatically set to the current date and time when a
        `RevenueConfiguration` instance is created.
        """
        revenue_configuration = RevenueConfigurationFactory(organization=self.organization)
        self.assertIsNotNone(revenue_configuration.start_date)

    def test_end_date_null(self):
        """
        Test that the `end_date` field can be null when creating a `RevenueConfiguration` instance.
        """
        revenue_configuration = RevenueConfigurationFactory(organization=self.organization, end_date=None)
        self.assertIsNone(revenue_configuration.end_date)

    def test_end_date_not_null(self):
        """
        Test that the `end_date` field cannot be null when creating a `RevenueConfiguration` instance.
        """
        with self.assertRaises(IntegrityError):
            RevenueConfigurationFactory(organization=self.organization, end_date=None)

    def test_course_code_max_length(self):
        """
        Test that attempting to create a `RevenueConfiguration` instance with a `course_code`
        that exceeds the maximum length raises a `ValidationError`.
        """
        long_course_code = "a" * 51
        with self.assertRaises(ValidationError):
            RevenueConfigurationFactory(organization=self.organization, course_code=long_course_code)

    def test_course_code_blank(self):
        """
        Test that the `course_code` field can be blank when creating a `RevenueConfiguration` instance.
        """
        revenue_configuration = RevenueConfigurationFactory(organization=self.organization, course_code="")
        self.assertEqual(revenue_configuration.course_code, "")

    def test_course_code_and_organization_null(self):
        """
        Test that attempting to create a `RevenueConfiguration` instance with both `course_code`
        and `organization` null raises a `ValidationError`.
        """
        with self.assertRaises(ValidationError):
            RevenueConfigurationFactory(organization=None, course_code=None)

    def test_organization_foreign_key(self):
        """
        Test that the `organization` field is a foreign key to the `Organization` model.
        """
        revenue_configuration = RevenueConfigurationFactory(organization=self.organization)
        self.assertEqual(revenue_configuration.organization, self.organization)

    def test_organization_related_name(self):
        """
        Test that the `related_name` argument for the `organization` field is set to `"revenue_organizations"`.
        """
        self.assertIn(self.organization)

    def test_organization_or_course_code_constraint(self):
        """
        Test that the `organization_or_course_code` constraint is enforced.
        """
        with self.assertRaises(IntegrityError):
            RevenueConfigurationFactory(organization=None, course_code=None)

    def test_end_date_equal_to_start_date(self):
        """
        Test that the `end_date` field can be equal to the `start_date` field when
        creating a `RevenueConfiguration` instance.
        """
        revenue_configuration = RevenueConfigurationFactory(
            organization=self.organization,
            start_date="2022-01-01 00:00:00",
            end_date="2022-01-01 00:00:00",
        )
        self.assertEqual(revenue_configuration.start_date, revenue_configuration.end_date)

    def test_end_date_greater_than_start_date(self):
        """
        Test that the `end_date` field can be greater than the `start_date` field when
        creating a `RevenueConfiguration` instance.
        """
        revenue_configuration = RevenueConfigurationFactory(
            organization=self.organization,
            start_date="2021-01-01 00:00:00",
            end_date="2022-01-01 00:00:00",
        )
        self.assertLess(revenue_configuration.start_date, revenue_configuration.end_date)
