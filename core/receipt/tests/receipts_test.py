from django.test import TestCase

from core.receipt.factories import ReceiptFactory, ReceiptLineFactory
from core.receipt.models import Receipt, ReceiptLine


class ReceiptModelTestCase(TestCase):
    def test_receipt_creation(self):
        receipt = ReceiptFactory()
        self.assertIsInstance(receipt, Receipt)

    def test_receipt_str_representation(self):
        receipt = ReceiptFactory(name="John Doe")
        self.assertEqual(str(receipt), "John Doe")

    def test_receipt_update(self):
        receipt = ReceiptFactory(name="Initial Name")
        new_name = "Updated Name"
        receipt.name = new_name
        receipt.save()
        updated_receipt = Receipt.objects.get(pk=receipt.pk)
        self.assertEqual(updated_receipt.name, new_name)

    def test_receipt_delete(self):
        receipt = ReceiptFactory()
        receipt_pk = receipt.pk
        receipt.delete()
        with self.assertRaises(Receipt.DoesNotExist):
            Receipt.objects.get(pk=receipt_pk)

    def test_receipt_read(self):
        receipt = ReceiptFactory()
        retrieved_receipt = Receipt.objects.get(pk=receipt.pk)
        self.assertEqual(receipt, retrieved_receipt)


class ReceiptLineModelTestCase(TestCase):
    def test_receipt_line_creation(self):
        receipt_line = ReceiptLineFactory()
        self.assertIsInstance(receipt_line, ReceiptLine)

    def test_receipt_line_str_representation(self):
        receipt_line = ReceiptLineFactory(description="Product A")
        self.assertEqual(str(receipt_line), "Product A")

    def test_receipt_line_update(self):
        receipt_line = ReceiptLineFactory(description="Initial Description")
        new_description = "Updated Description"
        receipt_line.description = new_description
        receipt_line.save()
        updated_receipt_line = ReceiptLine.objects.get(pk=receipt_line.pk)
        self.assertEqual(updated_receipt_line.description, new_description)

    def test_receipt_line_delete(self):
        receipt_line = ReceiptLineFactory()
        receipt_line_pk = receipt_line.pk
        receipt_line.delete()
        with self.assertRaises(ReceiptLine.DoesNotExist):
            ReceiptLine.objects.get(pk=receipt_line_pk)

    def test_receipt_line_read(self):
        receipt_line = ReceiptLineFactory()
        retrieved_receipt_line = ReceiptLine.objects.get(pk=receipt_line.pk)
        self.assertEqual(receipt_line, retrieved_receipt_line)
