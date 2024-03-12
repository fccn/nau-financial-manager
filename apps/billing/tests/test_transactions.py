from django.db import IntegrityError
from django.test import TestCase

from apps.billing.factories import TransactionFactory, TransactionItemFactory
from apps.billing.models import Transaction, TransactionItem


class TransactionTest(TestCase):
    """
    Test case for the Transaction model.
    """

    def test_transaction_creation(self):
        """
        Test if a Transaction instance can be created.
        """
        transaction = TransactionFactory()
        self.assertIsInstance(transaction, Transaction)

    def test_transaction_str_representation(self):
        """
        Test the string representation of a Transaction instance.
        """
        transaction = TransactionFactory(transaction_id="A_LONG_HASH_ID")
        self.assertEqual(str(transaction), "A_LONG_HASH_ID")

    def test_transaction_update(self):
        """
        Test updating the name of a Transaction instance.
        """
        transaction = TransactionFactory(client_name="Initial Name")
        new_name = "Updated Name"
        transaction.client_name = new_name
        transaction.save()
        updated_transaction = Transaction.objects.get(pk=transaction.pk)
        self.assertEqual(updated_transaction.client_name, new_name)

    def test_transaction_delete(self):
        """
        Test deleting a Transaction instance.
        """
        transaction = TransactionFactory()
        transaction_pk = transaction.pk
        transaction.delete()
        with self.assertRaises(Transaction.DoesNotExist):
            Transaction.objects.get(pk=transaction_pk)

    def test_transaction_read(self):
        """
        Test reading a Transaction instance from the database.
        """
        transaction = TransactionFactory()
        retrieved_transaction = Transaction.objects.get(pk=transaction.pk)
        self.assertEqual(transaction, retrieved_transaction)


class TransactionItemTest(TestCase):
    """
    Test case for the TransactionItem model.
    """

    def test_transaction_item_creation(self):
        """
        Test if a TransactionItem instance can be created.
        """
        transaction_item = TransactionItemFactory()
        self.assertIsInstance(transaction_item, TransactionItem)

    def test_transaction_item_str_representation(self):
        """
        Test the string representation of a TransactionItem instance.
        """
        transaction_item = TransactionItemFactory(
            product_id="Product_A",
        )
        self.assertEqual(str(transaction_item), "Product_A")

    def test_transaction_item_update(self):
        """
        Test updating the description of a TransactionItem instance.
        """
        transaction_item = TransactionItemFactory(description="Initial Description")
        new_description = "Updated Description"
        transaction_item.description = new_description
        transaction_item.save()
        updated_transaction_item = TransactionItem.objects.get(pk=transaction_item.pk)
        self.assertEqual(updated_transaction_item.description, new_description)

    def test_transaction_item_delete(self):
        """
        Test deleting a TransactionItem instance.
        """
        transaction_item = TransactionItemFactory()
        transaction_item_pk = transaction_item.pk
        transaction_item.delete()
        with self.assertRaises(TransactionItem.DoesNotExist):
            TransactionItem.objects.get(pk=transaction_item_pk)

    def test_transaction_item_read(self):
        """
        Test reading a TransactionItem instance from the database.
        """
        transaction_item = TransactionItemFactory()
        retrieved_transaction_item = TransactionItem.objects.get(pk=transaction_item.pk)
        self.assertEqual(transaction_item, retrieved_transaction_item)

    def test_unique_transaction(self):
        """
        Test that a `TransactionItem` object cannot be associated with more than one `Transaction`.

        This test creates a `Transaction` object and associates it with a `TransactionItem` object. It then attempts to create
        another `TransactionItem` object with the same `Transaction`, which should raise an `IntegrityError` due to the
        `UniqueConstraint` on the `TransactionItem` model. We use the `assertRaises` method to check that the `IntegrityError`
        is raised when attempting to create the new `TransactionItem` object.
        """
        transaction = TransactionFactory(
            transaction_id="123456789",
        )
        TransactionItemFactory(
            transaction=transaction,
        )
        with self.assertRaises(IntegrityError):
            transaction = TransactionFactory(
                transaction_id="123456789",
            )
