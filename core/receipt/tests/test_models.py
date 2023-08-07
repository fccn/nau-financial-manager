from django.test import TestCase
from core.receipt.models import Receipt, ReceiptLine
from core.receipt.tests.models_factory import ReceiptFactory, ReceiptLineFactory


class ReceiptModelTestCase(TestCase):
    def test_receipt_creation(self):
        receipt = ReceiptFactory()
        self.assertIsInstance(receipt, Receipt)

    def test_receipt_str_representation(self):
        receipt = ReceiptFactory(name="John Doe")
        self.assertEqual(str(receipt), "John Doe")


class ReceiptLineModelTestCase(TestCase):
    def test_receipt_line_creation(self):
        receipt_line = ReceiptLineFactory()
        self.assertIsInstance(receipt_line, ReceiptLine)

    def test_receipt_line_str_representation(self):
        receipt_line = ReceiptLineFactory(description="Product A")
        self.assertEqual(str(receipt_line), "Product A")
