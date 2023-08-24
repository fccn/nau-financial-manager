from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from core.shared_revenue.factories import PartnershipLevelFactory
from core.shared_revenue.models import PartnershipLevel


class PartnershipLevelTestCase(TestCase):
    def setUp(self):
        self.partnership_level = PartnershipLevelFactory()

    def test_str_method(self):
        """
        Test the `__str__` method of the `PartnershipLevel` model.
        """
        self.assertEqual(
            str(self.partnership_level), f"{self.partnership_level.name} - {self.partnership_level.percentage}"
        )

    def test_partnership_level_name_already_exists(self):
        """
        Test that attempting to create a `PartnershipLevel` instance with a duplicate `name` raises an `Exception`.
        """
        with self.assertRaises(Exception):
            PartnershipLevelFactory(name=self.partnership_level.name)

    def test_partnership_level_percentage_unique(self):
        """
        Test that attempting to create a `PartnershipLevel` instance with a duplicate `value` raises an `Exception`.
        """
        with self.assertRaises(Exception):
            PartnershipLevelFactory(percentage=self.partnership_level.percentage)

    def test_name_max_length(self):
        """
        Test that attempting to create a `PartnershipLevel` instance with a `name` that exceeds the maximum length raises an `Exception`.
        """
        max_length = PartnershipLevel._meta.get_field("name").max_length
        long_name = "a" * (max_length + 1)
        with self.assertRaises(Exception):
            PartnershipLevelFactory(name=long_name)

    def test_percentagem_number_is_valid(self):
        """
        Test that attempting to create a `PartnershipLevel` instance with a `percentage`
        that exceeds the maximum number of digits raises a `ValidationError`.
        """
        max_digits = PartnershipLevel._meta.get_field("percentage").max_digits
        decimal_places = PartnershipLevel._meta.get_field("percentage").decimal_places
        long_value = Decimal("9" * (max_digits - decimal_places + 1) + "." + "9" * decimal_places)
        with self.assertRaises(ValidationError):
            PartnershipLevel.objects.create(name="Test Partnership Level 2", percentage=long_value)

    def test_percentage_decimal_places(self):
        """
        Test that attempting to create a `PartnershipLevel` instance with a `percentage`
        that exceeds the maximum number of decimal places raises a `ValidationError`.
        """
        max_digits = PartnershipLevel._meta.get_field("percentage").max_digits
        decimal_places = PartnershipLevel._meta.get_field("percentage").decimal_places
        long_value = Decimal("9" * (max_digits - decimal_places) + "." + "9" * (decimal_places + 1))
        with self.assertRaises(ValidationError):
            PartnershipLevelFactory(name="Test Partnership Level 3", percentage=long_value)

    def test_percentage_max_value(self):
        """
        Test that attempting to create a `PartnershipLevel` instance with a `percentage` greater
        than 1 raises a `ValidationError`.
        """
        with self.assertRaises(ValidationError):
            PartnershipLevelFactory(name="Test Partnership Level 2", percentage=Decimal("1.1"))

    def test_percentage_min_value(self):
        """
        Test that attempting to create a `PartnershipLevel` instance with a
        `percentage` less than 0 raises a `ValidationError`.
        """
        with self.assertRaises(ValidationError):
            PartnershipLevelFactory(name="Test Partnership Level 3", percentage=Decimal("-0.1"))
