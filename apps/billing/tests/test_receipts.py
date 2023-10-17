from decimal import Decimal

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
        transaction = TransactionFactory(name="John Doe")
        self.assertEqual(str(transaction), "John Doe")

    def test_transaction_update(self):
        """
        Test updating the name of a Transaction instance.
        """
        transaction = TransactionFactory(name="Initial Name")
        new_name = "Updated Name"
        transaction.name = new_name
        transaction.save()
        updated_transaction = Transaction.objects.get(pk=transaction.pk)
        self.assertEqual(updated_transaction.name, new_name)

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
        transaction_item = TransactionItemFactory(description="Product A")
        self.assertEqual(str(transaction_item), "Product A")

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

    def test_unique_transaction_item_constraint(self):
        """
        Test that a `TransactionItem` object cannot be associated with more than one `Transaction`.

        This test creates a `Transaction` object and associates it with a `TransactionItem` object. It then attempts to create
        another `TransactionItem` object with the same `Transaction`, which should raise an `IntegrityError` due to the
        `UniqueConstraint` on the `TransactionItem` model. We use the `assertRaises` method to check that the `IntegrityError`
        is raised when attempting to create the new `TransactionItem` object.
        """
        transaction = TransactionFactory(
            name="John Doe",
            email="johndoe@example.com",
            address="123 Main St",
            vat_identification_country="US",
            vat_identification_number="123456789",
            total_amount_exclude_vat=Decimal("100.00"),
            total_amount_include_vat=Decimal("110.00"),
            transaction_link="https://example.com/transaction",
            transaction_document_id="123456789",
        )
        TransactionItemFactory(
            transaction=transaction,
            description="Item 1",
            quantity=2,
            vat_tax=Decimal("10.00"),
            amount_exclude_vat=Decimal("50.00"),
            amount_include_vat=Decimal("55.00"),
            organization_code="ORG1",
            course_code="COURSE1",
            course_id="123456",
        )
        with self.assertRaises(IntegrityError):
            TransactionItemFactory(
                transaction=transaction,
                description="Item 2",
                quantity=1,
                vat_tax=Decimal("5.00"),
                amount_exclude_vat=Decimal("25.00"),
                amount_include_vat=Decimal("27.50"),
                organization_code="ORG2",
                course_code="COURSE2",
                course_id="654321",
            )
