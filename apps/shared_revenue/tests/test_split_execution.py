from collections.abc import Callable
from decimal import Decimal

import factory
from django.test import TestCase
from django.utils import timezone

from apps.billing.factories import Transaction, TransactionFactory, TransactionItem, TransactionItemFactory
from apps.organization.factories import Organization, OrganizationFactory
from apps.shared_revenue.factories import RevenueConfigurationFactory
from apps.shared_revenue.models import RevenueConfiguration
from apps.shared_revenue.services.split_execution import SplitExecutionService


class SplitExecutionServiceTestCase(TestCase):
    def setUp(self) -> None:
        """
        Defines and start the entire test base.

        - nau percentage
        - partner_percentage
        - list of organizations
        - list of transactions
        - list of transaction items
        - list of configurations
        - start and end dates parameters
        """

        self.nau_percentage = round(Decimal(0.30), 2)
        self.partner_percentage = round(Decimal(0.70), 2)

        self.organizations: list[Organization] = OrganizationFactory.create_batch(5)
        self.transactions: list[Transaction] = []
        self.transaction_items: list[TransactionItem] = []
        self.configurations: list[RevenueConfiguration] = []

        for organization in self.organizations:
            generated_transactions = TransactionFactory.create_batch(5)
            self.transactions += generated_transactions

            for transaction in generated_transactions:
                item = TransactionItemFactory.create(
                    organization_code=organization.short_name,
                    transaction=transaction,
                )
                self.transaction_items.append(item)

            configuration = RevenueConfigurationFactory.create(
                organization=organization,
                product_id=item.product_id,
                partner_percentage=self.partner_percentage,
                start_date=factory.Faker(
                    "date_time_between",
                    start_date="-6d",
                    end_date="+1d",
                    tzinfo=timezone.get_current_timezone(),
                ),
            )
            self.configurations.append(configuration)

        start_date = (timezone.now() - timezone.timedelta(days=11)).isoformat()
        end_date = (timezone.now() + timezone.timedelta(days=30)).replace(hour=23, minute=59, second=59).isoformat()

        self.options = {
            "start_date": start_date,
            "end_date": end_date,
        }

    def test_execute_split_without_filters(self):
        """
        Should validate that it is possible to calculate all the transactions
        based on the given dates.
        """

        split_result = SplitExecutionService(
            start_date=self.options["start_date"],
            end_date=self.options["end_date"],
        ).execute_split_steps()

        results = split_result[0]
        configurations = split_result[1]

        self.assertTrue(len(results) > 0)
        self.assertTrue(len(configurations) > 0)

    def test_filter_by_organization(self):
        """
        Should validate that it is possible to calculate all the transactions based on
        the given dates by filtering for only transactions of a certain organization.
        """

        kwargs = {"organization_code": self.organizations[0].short_name}
        split_result = SplitExecutionService(
            start_date=self.options["start_date"],
            end_date=self.options["end_date"],
        ).execute_split_steps(**kwargs)

        results = split_result[0]
        configurations = split_result[1]

        if all([len(results) > 0, len(configurations) > 0]):
            for result in results:
                self.assertEqual(result["organization"], self.organizations[0].short_name)

            for configuration in configurations:
                self.assertEqual(configuration["organization"], self.organizations[0].short_name)

    def test_filter_by_product(self):
        """
        Should validate that it is possible to calculate all the transactions based on
        the given dates by filtering for only transactions of a certain product.
        """

        kwargs = {"product_id": self.transaction_items[0].product_id}
        split_result = SplitExecutionService(
            start_date=self.options["start_date"],
            end_date=self.options["end_date"],
        ).execute_split_steps(**kwargs)

        results = split_result[0]
        configurations = split_result[1]

        for result in results:
            self.assertEqual(result["product_id"], self.transaction_items[0].product_id)

        for configuration in configurations:
            self.assertEqual(configuration["product_id"], self.transaction_items[0].product_id)

    def test_filter_by_organization_and_product(self):
        """
        Should validate that it is possible to calculate all the transactions based on
        the given dates by filtering for only transactions of certain combined organization and product.
        """

        kwargs = {
            "organization_code": self.organizations[1].short_name,
            "product_id": self.transaction_items[1].product_id,
        }
        split_result = SplitExecutionService(
            start_date=self.options["start_date"],
            end_date=self.options["end_date"],
        ).execute_split_steps(**kwargs)

        results = split_result[0]
        configurations = split_result[1]

        for result in results:
            self.assertEqual(result["product_id"], self.transaction_items[1].product_id)
            self.assertEqual(result["organization"], self.organizations[1].short_name)

        for configuration in configurations:
            self.assertEqual(configuration["product_id"], self.transaction_items[1].product_id)
            self.assertEqual(result["organization"], self.organizations[1].short_name)

    def test_calculate_transactions_results(self):
        """
        Should validate the calculated result of each transaction based on the defined
        parameters in the `setUp` method, every result should respect the expected value
        """
        split_result = SplitExecutionService(
            start_date=self.options["start_date"],
            end_date=self.options["end_date"],
        ).execute_split_steps()

        results = split_result[0]
        configurations = split_result[1]

        self.assertTrue(len(results) > 0)
        self.assertTrue(len(configurations) > 0)

        for result in results:
            current_item: Callable[[TransactionItem], bool] = lambda i: [
                i.product_id,
                i.organization_code,
                i.transaction.transaction_id,
            ] == [
                result["product_id"],
                result["organization"],
                result["transaction_id"],
            ]

            item = [i for i in self.transaction_items if current_item(i=i)][0]

            self.assertEqual(result["percentage_for_organization"], self.partner_percentage)
            self.assertEqual(
                result["amount_for_organization_including_vat"],
                (item.unit_price_incl_vat * self.partner_percentage) * item.quantity,
            )
            self.assertEqual(
                result["amount_for_organization_exclude_vat"],
                (item.unit_price_excl_vat * self.partner_percentage) * item.quantity,
            )

            self.assertEqual(result["percentage_for_nau"], self.nau_percentage)
            self.assertEqual(
                result["amount_for_nau_including_vat"],
                (item.unit_price_incl_vat * self.nau_percentage) * item.quantity,
            )
            self.assertEqual(
                result["amount_for_nau_exclude_vat"], (item.unit_price_excl_vat * self.nau_percentage) * item.quantity
            )

    def test_split_includes_every_item_of_a_multi_item_transaction(self):
        """
        Regression test for issue #336.

        A transaction with more than one item must have every item represented in the
        split result, including items that belong to a different organization than the first one.
        """
        first_organization, second_organization = OrganizationFactory.create_batch(2)

        transaction = TransactionFactory.create()
        first_item = TransactionItemFactory.create(
            organization_code=first_organization.short_name,
            transaction=transaction,
        )
        second_item = TransactionItemFactory.create(
            organization_code=second_organization.short_name,
            transaction=transaction,
        )
        for organization, item in [(first_organization, first_item), (second_organization, second_item)]:
            RevenueConfigurationFactory.create(
                organization=organization,
                product_id=item.product_id,
                partner_percentage=self.partner_percentage,
                start_date=transaction.transaction_date - timezone.timedelta(days=1),
                end_date=transaction.transaction_date + timezone.timedelta(days=1),
            )

        split_result = SplitExecutionService(
            start_date=self.options["start_date"],
            end_date=self.options["end_date"],
        ).execute_split_steps()

        results = [result for result in split_result[0] if result["transaction_id"] == transaction.transaction_id]

        self.assertEqual(len(results), 2)
        self.assertEqual(
            {(result["product_id"], result["organization"]) for result in results},
            {
                (first_item.product_id, first_organization.short_name),
                (second_item.product_id, second_organization.short_name),
            },
        )
        for item in [first_item, second_item]:
            result = next(r for r in results if r["product_id"] == item.product_id)
            self.assertEqual(
                result["amount_for_organization_including_vat"],
                (item.unit_price_incl_vat * self.partner_percentage) * item.quantity,
            )
