from decimal import Decimal

from django.db import IntegrityError
from django.test import TestCase

from apps.billing.factories import ReceiptFactory, ReceiptItemFactory
from apps.billing.models import Receipt, ReceiptItem


class ReceiptTest(TestCase):
    """
    Test case for the Receipt model.
    """

    def test_receipt_creation(self):
        """
        Test if a Receipt instance can be created.
        """
        receipt = ReceiptFactory()
        self.assertIsInstance(receipt, Receipt)

    def test_receipt_str_representation(self):
        """
        Test the string representation of a Receipt instance.
        """
        receipt = ReceiptFactory(name="John Doe")
        self.assertEqual(str(receipt), "John Doe")

    def test_receipt_update(self):
        """
        Test updating the name of a Receipt instance.
        """
        receipt = ReceiptFactory(name="Initial Name")
        new_name = "Updated Name"
        receipt.name = new_name
        receipt.save()
        updated_receipt = Receipt.objects.get(pk=receipt.pk)
        self.assertEqual(updated_receipt.name, new_name)

    def test_receipt_delete(self):
        """
        Test deleting a Receipt instance.
        """
        receipt = ReceiptFactory()
        receipt_pk = receipt.pk
        receipt.delete()
        with self.assertRaises(Receipt.DoesNotExist):
            Receipt.objects.get(pk=receipt_pk)

    def test_receipt_read(self):
        """
        Test reading a Receipt instance from the database.
        """
        receipt = ReceiptFactory()
        retrieved_receipt = Receipt.objects.get(pk=receipt.pk)
        self.assertEqual(receipt, retrieved_receipt)


class ReceiptItemTest(TestCase):
    """
    Test case for the ReceiptItem model.
    """

    def test_receipt_item_creation(self):
        """
        Test if a ReceiptItem instance can be created.
        """
        receipt_line = ReceiptItemFactory()
        self.assertIsInstance(receipt_line, ReceiptItem)

    def test_receipt_item_str_representation(self):
        """
        Test the string representation of a ReceiptItem instance.
        """
        receipt_line = ReceiptItemFactory(description="Product A")
        self.assertEqual(str(receipt_line), "Product A")

    def test_receipt_item_update(self):
        """
        Test updating the description of a ReceiptItem instance.
        """
        receipt_line = ReceiptItemFactory(description="Initial Description")
        new_description = "Updated Description"
        receipt_line.description = new_description
        receipt_line.save()
        updated_receipt_line = ReceiptItem.objects.get(pk=receipt_line.pk)
        self.assertEqual(updated_receipt_line.description, new_description)

    def test_receipt_item_delete(self):
        """
        Test deleting a ReceiptItem instance.
        """
        receipt_line = ReceiptItemFactory()
        receipt_line_pk = receipt_line.pk
        receipt_line.delete()
        with self.assertRaises(ReceiptItem.DoesNotExist):
            ReceiptItem.objects.get(pk=receipt_line_pk)

    def test_receipt_item_read(self):
        """
        Test reading a ReceiptItem instance from the database.
        """
        receipt_line = ReceiptItemFactory()
        retrieved_receipt_line = ReceiptItem.objects.get(pk=receipt_line.pk)
        self.assertEqual(receipt_line, retrieved_receipt_line)

    def test_unique_receipt_item_constraint(self):
        """
        Test that a `ReceiptItem` object cannot be associated with more than one `Receipt`.

        This test creates a `Receipt` object and associates it with a `ReceiptItem` object. It then attempts to create
        another `ReceiptItem` object with the same `Receipt`, which should raise an `IntegrityError` due to the
        `UniqueConstraint` on the `ReceiptItem` model. We use the `assertRaises` method to check that the `IntegrityError`
        is raised when attempting to create the new `ReceiptItem` object.
        """
        receipt = ReceiptFactory(
            name="John Doe",
            email="johndoe@example.com",
            address="123 Main St",
            vat_identification_country="US",
            vat_identification_number="123456789",
            total_amount_exclude_vat=Decimal("100.00"),
            total_amount_include_vat=Decimal("110.00"),
            receipt_link="https://example.com/receipt",
            receipt_document_id="123456789",
        )
        ReceiptItemFactory(
            receipt=receipt,
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
            ReceiptItemFactory(
                receipt=receipt,
                description="Item 2",
                quantity=1,
                vat_tax=Decimal("5.00"),
                amount_exclude_vat=Decimal("25.00"),
                amount_include_vat=Decimal("27.50"),
                organization_code="ORG2",
                course_code="COURSE2",
                course_id="654321",
            )
