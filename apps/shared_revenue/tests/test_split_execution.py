from datetime import datetime, timedelta
from decimal import Decimal

from django.test import TestCase

from apps.billing.factories import Transaction, TransactionFactory, TransactionItem, TransactionItemFactory
from apps.organization.factories import Organization, OrganizationFactory
from apps.shared_revenue.factories import RevenueConfigurationFactory
from apps.shared_revenue.services.split_execution import SplitExecutionService, SplitResult


class SplitExecutionServiceTestCase(TestCase):
    def setUp(self) -> None:
        self.nau_percentage = round(Decimal(0.30), 2)
        self.partner_percentage = round(Decimal(0.70), 2)

        self.organizations: list[Organization] = OrganizationFactory.create_batch(5)
        self.transactions: list[Transaction] = []
        self.transaction_items: list[TransactionItem] = []

        for organization in self.organizations:
            transaction = TransactionFactory.create()
            self.transactions.append(transaction)

            item = TransactionItemFactory.create(
                organization_code=organization.short_name,
                transaction=transaction,
            )
            self.transaction_items.append(item)

            RevenueConfigurationFactory.create(
                organization=organization,
                product_id=item.product_id,
                partner_percentage=self.partner_percentage,
            )

        self.columns = [
            "product_name",
            "transaction_date",
            "total_amount_include_vat",
            "total_amount_exclude_vat",
            "organization_code",
            "amount_for_nau",
            "amount_for_organization",
        ]

        self.split_result: SplitResult = SplitExecutionService(
            start_date=datetime.now() - timedelta(days=1),
            end_date=datetime.now() + timedelta(days=2),
        ).execute_split_steps()

    def test_validate_the_split_value_result(self):

        for split_result in self.split_result.results:
            self.assertEqual(
                split_result["amount_for_nau"], split_result["total_amount_include_vat"] * self.nau_percentage
            )
            self.assertEqual(
                split_result["amount_for_organization"],
                split_result["total_amount_include_vat"] * self.partner_percentage,
            )

    def test_split_result_instance(self):
        self.assertEqual(self.split_result.file_name, "test_file")
        for split_result in self.split_result.results:
            self.assertEqual(self.columns, list(split_result.keys()))
        #
        # self.assertEqual(self.split_result.columns, self.columns)

    def test_filter_transaction_items(self):
        pass

    def test_filter_revenue_configurations(self):
        pass

    def test_assembly_each_result(self):
        pass

    def test_calculate_transactions(self):
        pass

    def test_execute_split_steps(self):
        pass

    def tearDown(self) -> None:
        return super().tearDown()
