from datetime import datetime, timedelta
from decimal import Decimal

import factory
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.organization.factories import OrganizationFactory
from apps.shared_revenue.factories import RevenueConfigurationFactory
from apps.shared_revenue.models import RevenueConfiguration


class RevenueConfigurationTestCase(TestCase):
    def setUp(self):
        self.organization = OrganizationFactory()
        self.revenue_configuration = RevenueConfigurationFactory(organization=self.organization)

    def test_str_method(self):
        """
        Should validate that the `RevenueConfiguration.__str__` method returns the correct parameters in the correct sequence.
        """

        self.assertEqual(
            str(self.revenue_configuration),
            f"{self.organization} - {self.revenue_configuration.product_id} - {self.revenue_configuration.partner_percentage}",
        )

    def test_valid_partner_percentage(self):
        """
        Should validate that the `partner_percentage` is between 0 and 1.
        """

        self.assertGreaterEqual(self.revenue_configuration.partner_percentage, 0)
        self.assertLessEqual(self.revenue_configuration.partner_percentage, 1)

    def test_has_concurrent_revenue_configuration_with_dates(self):
        """
        Should raise an error of type `ValidationError`, it validates that
        already exists a `RevenueConfiguration` for this `Organization` and `product_id`
        for the concurrent period of time.
        """

        with self.assertRaisesMessage(
            expected_exception=ValidationError,
            expected_message="There is a concurrent revenue configuration in this moment",
        ):
            RevenueConfigurationFactory(
                start_date=factory.Faker(
                    "date_time_between", start_date="+1d", end_date="+20d", tzinfo=timezone.get_current_timezone()
                ),
                end_date=factory.Faker(
                    "date_time_between", start_date="+30d", end_date="+69d", tzinfo=timezone.get_current_timezone()
                ),
                product_id=self.revenue_configuration.product_id,
                organization=self.organization,
                partner_percentage=0,
            )

    def test_has_concurrent_revenue_configuration_with_just_start_date(self):
        """
        Should raise an error of type `ValidationError`, it validates that
        already exists a `RevenueConfiguration` for this `Organization` and `product_id`
        for the concurrent period of time, considering that the attempt is to save a None `end_date`.
        """

        with self.assertRaisesMessage(
            expected_exception=ValidationError,
            expected_message="There is a concurrent revenue configuration in this moment",
        ):
            RevenueConfigurationFactory(
                start_date=factory.Faker(
                    "date_time_between", start_date="+1d", end_date="+20d", tzinfo=timezone.get_current_timezone()
                ),
                end_date=None,
                product_id=self.revenue_configuration.product_id,
                organization=self.organization,
                partner_percentage=0,
            )

    def test_has_concurrent_revenue_configuration_with_just_end_date(self):
        """
        Should raise an error of type `ValidationError`, it validates that
        already exists a `RevenueConfiguration` for this `Organization` and `product_id`
        for concurrent period of time, considering that the attempt is to save a None `start_date`.
        """

        with self.assertRaisesMessage(
            expected_exception=ValidationError,
            expected_message="There is a concurrent revenue configuration in this moment",
        ):
            RevenueConfigurationFactory(
                start_date=None,
                end_date=factory.Faker(
                    "date_time_between", start_date="+30d", end_date="+69d", tzinfo=timezone.get_current_timezone()
                ),
                product_id=self.revenue_configuration.product_id,
                organization=self.organization,
                partner_percentage=0,
            )

    def test_has_concurrent_revenue_configuration_with_no_dates(self):
        """
        Should raise an error of type `ValidationError`, it validates that
        already exists a `RevenueConfiguration` for this `Organization` and `product_id`
        in the concurrent period of time, considering that the attempt is to save
        as None the `start_date` and `end_date` parameters.
        """

        with self.assertRaisesMessage(
            expected_exception=ValidationError,
            expected_message="There is a concurrent revenue configuration in this moment",
        ):
            RevenueConfigurationFactory(
                start_date=None,
                end_date=None,
                product_id=self.revenue_configuration.product_id,
                organization=self.organization,
                partner_percentage=0,
            )

    def test_has_no_concurrent_revenue_configuration(self):
        """
        Should register a new `RevenueConfiguration`, it validades that this attempt
        is to save a new configuration which will not impact on the current, or any other configuration.
        """

        new_configuration = RevenueConfigurationFactory(
            start_date=factory.Faker(
                "date_time_between", start_date="+71d", end_date="+80d", tzinfo=timezone.get_current_timezone()
            ),
            end_date=factory.Faker(
                "date_time_between", start_date="+81d", end_date="+90d", tzinfo=timezone.get_current_timezone()
            ),
            organization=self.organization,
            product_id=self.revenue_configuration.product_id,
            partner_percentage=0,
        )

        self.assertNotEqual(new_configuration.id, self.revenue_configuration.id)
        self.assertEqual(new_configuration.organization, self.revenue_configuration.organization)
        self.assertEqual(new_configuration.product_id, self.revenue_configuration.product_id)
        self.assertTrue(new_configuration.start_date != self.revenue_configuration.start_date)
        self.assertTrue(new_configuration.end_date != self.revenue_configuration.end_date)

    def test_future_configuration_creation(self):
        """
        Should register a new `RevenueConfiguration`, it validades that this attempt
        is to save a future configuration considering as None the `end_date`, which will not impact
        on the current, or any other configuration.

        In the last line of this test function, the new configuration is deleted,
        the reason for that is because leaving this configuration created, it will
        prevent the creation of another new one and break the other tests. This behavior
        is right, as expected it is not possible to create another one, if there are a concurrent
        configuration, then it's deleted because the testing needs to continue.
        """

        new_configuration = RevenueConfigurationFactory(
            start_date=factory.Faker(
                "date_time_between", start_date="+82d", end_date="+90d", tzinfo=timezone.get_current_timezone()
            ),
            end_date=None,
            organization=self.organization,
            product_id=self.revenue_configuration.product_id,
            partner_percentage=0,
        )
        self.assertNotEqual(new_configuration.id, self.revenue_configuration.id)
        self.assertEqual(new_configuration.organization, self.revenue_configuration.organization)
        self.assertEqual(new_configuration.product_id, self.revenue_configuration.product_id)
        self.assertTrue(new_configuration.start_date > self.revenue_configuration.start_date)
        self.assertIsNone(new_configuration.end_date)
        new_configuration.delete()

    def test_older_configuration_creation(self):
        """
        Should register a new `RevenueConfiguration`, it validades that this attempt
        is to save a older configuration, which will not impact on the current, or any other configuration.
        """

        new_configuration = RevenueConfigurationFactory(
            start_date=factory.Faker(
                "date_time_between", start_date="-100d", end_date="-98d", tzinfo=timezone.get_current_timezone()
            ),
            end_date=factory.Faker(
                "date_time_between", start_date="-97d", end_date="-95d", tzinfo=timezone.get_current_timezone()
            ),
            organization=self.organization,
            product_id=self.revenue_configuration.product_id,
            partner_percentage=0,
        )
        self.assertNotEqual(new_configuration.id, self.revenue_configuration.id)
        self.assertEqual(new_configuration.organization, self.revenue_configuration.organization)
        self.assertEqual(new_configuration.product_id, self.revenue_configuration.product_id)
        self.assertTrue(new_configuration.start_date < self.revenue_configuration.start_date)
        self.assertTrue(new_configuration.end_date < self.revenue_configuration.start_date)

    def test_edit_configuration(self):
        """
        Should edit a `RevenueConfiguration`, it validades that this attempt
        is to edit an existing configuration in a way that will not impact on the current,
        or any other configuration.
        """

        new_start_date = datetime.now(tz=timezone.get_current_timezone()) - timedelta(days=3)
        new_end_date = datetime.now(tz=timezone.get_current_timezone()) - timedelta(days=1)

        self.assertEqual(type(self.revenue_configuration.start_date), datetime)
        self.assertEqual(type(self.revenue_configuration.end_date), datetime)
        self.assertNotEqual(self.revenue_configuration.start_date, new_start_date)
        self.assertNotEqual(self.revenue_configuration.end_date, new_end_date)
        self.assertNotEqual(self.revenue_configuration.product_id, "new_product_id")
        self.assertNotEqual(self.revenue_configuration.partner_percentage, 0.69)

        self.revenue_configuration.start_date = new_start_date
        self.revenue_configuration.end_date = new_end_date
        self.revenue_configuration.partner_percentage = 0.69
        self.revenue_configuration.product_id = "new_product_id"

        self.assertEqual(type(self.revenue_configuration.start_date), datetime)
        self.assertEqual(type(self.revenue_configuration.end_date), datetime)
        self.assertEqual(self.revenue_configuration.start_date, new_start_date)
        self.assertEqual(self.revenue_configuration.end_date, new_end_date)
        self.assertEqual(self.revenue_configuration.partner_percentage, 0.69)
        self.assertEqual(self.revenue_configuration.product_id, "new_product_id")
        self.assertEqual(type(self.revenue_configuration), RevenueConfiguration)

    def test_edit_has_concurrent_revenue_configuration(self):
        """
        Should raise an error of type `ValidationError`, it validades that is not possible to edit
        an existing configuration in a way that will impact on the current, or any other configuration.
        """

        with self.assertRaisesMessage(
            expected_exception=ValidationError,
            expected_message="There is a concurrent revenue configuration in this moment",
        ):
            new_configuration = RevenueConfigurationFactory(
                start_date=factory.Faker(
                    "date_time_between", start_date="-10d", end_date="-5d", tzinfo=timezone.get_current_timezone()
                ),
                end_date=factory.Faker(
                    "date_time_between", start_date="-4d", end_date="-1d", tzinfo=timezone.get_current_timezone()
                ),
                organization=self.organization,
                product_id=self.revenue_configuration.product_id,
                partner_percentage=0,
            )

            new_start_date = new_configuration.start_date + timedelta(days=1)
            new_end_date = new_configuration.end_date - timedelta(days=1)

            self.assertEqual(type(new_start_date), datetime)
            self.assertEqual(type(new_end_date), datetime)
            self.assertEqual(type(new_configuration.start_date), datetime)
            self.assertEqual(type(new_configuration.end_date), datetime)
            self.assertEqual(type(self.revenue_configuration.start_date), datetime)
            self.assertEqual(type(self.revenue_configuration.end_date), datetime)
            self.assertEqual(type(new_configuration), RevenueConfiguration)

            self.assertNotEqual(self.revenue_configuration.start_date, new_start_date)
            self.assertNotEqual(self.revenue_configuration.end_date, new_end_date)
            self.assertNotEqual(new_configuration.start_date, self.revenue_configuration.start_date)
            self.assertNotEqual(new_configuration.end_date, self.revenue_configuration.end_date)

            self.revenue_configuration.start_date = new_start_date
            self.revenue_configuration.end_date = new_end_date

            self.assertEqual(type(self.revenue_configuration), RevenueConfiguration)
            self.revenue_configuration.save()

    def test_check_partner_percentage_with_error(self):
        """
        Should raise an error of type `ValidationError`, it validades that is not possible to create
        a configuration that exceeds 100% of partners percentage
        """

        with self.assertRaisesMessage(
            expected_exception=ValidationError,
            expected_message="The partner percentage exceeds 100%",
        ):
            self.revenue_configuration.partner_percentage = Decimal(0.7)
            self.revenue_configuration.save()

            RevenueConfigurationFactory(
                product_id=self.revenue_configuration.product_id,
                partner_percentage=Decimal(0.31),
            )

    def test_check_partner_percentage_with_success(self):
        """
        Should create a new configuration, it validates that is
        possible to register a new configuration when does not exceed
        100% in the `partner_percentage`'s calculation.
        """

        self.revenue_configuration.partner_percentage = Decimal(0.71)
        self.revenue_configuration.save()

        new_configuration = RevenueConfigurationFactory(
            product_id=self.revenue_configuration.product_id,
            partner_percentage=Decimal(0.29),
        )
        new_configuration.delete()
