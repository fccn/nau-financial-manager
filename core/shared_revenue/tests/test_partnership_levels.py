from django.test import TestCase

from core.shared_revenue.factories import PartnershipLevelFactory
from core.shared_revenue.models import PartnershipLevel


class PartnershipLevelTestCase(TestCase):
    def setUp(self):
        self.partnership_level = PartnershipLevelFactory()

    def test_str_method(self):
        self.assertEqual(
            str(self.partnership_level), f"{self.partnership_level.name} - {self.partnership_level.value}"
        )

    def test_name_unique_constraint(self):
        with self.assertRaises(Exception):
            PartnershipLevelFactory(name=self.partnership_level.name)

    def test_value_unique_constraint(self):
        with self.assertRaises(Exception):
            PartnershipLevelFactory(value=self.partnership_level.value)

    def test_name_max_length(self):
        max_length = PartnershipLevel._meta.get_field("name").max_length
        long_name = "a" * (max_length + 1)
        with self.assertRaises(Exception):
            PartnershipLevelFactory(name=long_name)

    def test_value_max_digits(self):
        max_digits = PartnershipLevel._meta.get_field("value").max_digits
        decimal_places = PartnershipLevel._meta.get_field("value").decimal_places
        long_value = "9" * (max_digits - decimal_places + 1) + "." + "9" * decimal_places
        with self.assertRaises(Exception):
            PartnershipLevelFactory(value=long_value)

    def test_value_decimal_places(self):
        max_digits = PartnershipLevel._meta.get_field("value").max_digits
        decimal_places = PartnershipLevel._meta.get_field("value").decimal_places
        long_value = "9" * (max_digits - decimal_places) + "." + "9" * (decimal_places + 1)
        with self.assertRaises(Exception):
            PartnershipLevelFactory(value=long_value)
