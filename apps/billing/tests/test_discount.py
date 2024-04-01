import decimal
import logging

from django.test import TestCase

from apps.billing.factories import TransactionFactory, TransactionItemFactory

log = logging.getLogger(__name__)


class DiscountTest(TestCase):
    """
    Test the discount
    """

    def test_discount_transaction_no_all_zero(self):
        """
        Test the discount model with discount with zero.
        """
        transaction = TransactionFactory.build()
        item = TransactionItemFactory.build(
            transaction=transaction, discount_excl_tax=decimal.Decimal(0.00), discount_incl_tax=decimal.Decimal(0.00)
        )
        print(item.discount_incl_tax)
        print(item.unit_price_incl_vat)
        self.assertEqual(item.discount_rate, 0.00)

    def test_discount_transaction_some_discount(self):
        """
        Test discount value with including vat fields.
        """
        transaction = TransactionFactory.build()
        item = TransactionItemFactory.build(
            transaction=transaction, unit_price_incl_vat=decimal.Decimal(9.00), discount_incl_tax=decimal.Decimal(1.00)
        )
        self.assertEqual(item.discount_rate, round(decimal.Decimal(0.10), 2))

    def test_discount_transaction_some_discount_percentage(self):
        """
        Test discount value like a percentage.
        """
        transaction = TransactionFactory.build()
        item = TransactionItemFactory.build(
            transaction=transaction, unit_price_incl_vat=decimal.Decimal(4.00), discount_incl_tax=decimal.Decimal(1.00)
        )
        self.assertEqual(item.discount_rate * 100, 20)
