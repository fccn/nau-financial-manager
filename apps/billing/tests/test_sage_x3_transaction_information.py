from django.test import TestCase

from apps.billing.factories import SageX3TransactionInformationFactory
from apps.billing.models import SageX3TransactionInformation


class SageX3TransactionInformationTest(TestCase):
    def setUp(self):
        self.sage_x3_transaction_info = SageX3TransactionInformationFactory.create(retries=0)

    def test_create_sage_x3_transaction_info(self):
        self.assertIsInstance(self.sage_x3_transaction_info, SageX3TransactionInformation)

    def test_retrieve_sage_x3_transaction_info(self):
        retrieved_info = SageX3TransactionInformation.objects.get(id=self.sage_x3_transaction_info.id)
        self.assertEqual(retrieved_info, self.sage_x3_transaction_info)

    def test_update_sage_x3_transaction_info(self):
        self.sage_x3_transaction_info.status = "updated_status"
        self.sage_x3_transaction_info.save()
        retrieved_info = SageX3TransactionInformation.objects.get(id=self.sage_x3_transaction_info.id)
        self.assertEqual(retrieved_info.status, "updated_status")

    def test_delete_sage_x3_transaction_info(self):
        self.sage_x3_transaction_info.delete()
        with self.assertRaises(SageX3TransactionInformation.DoesNotExist):
            SageX3TransactionInformation.objects.get(id=self.sage_x3_transaction_info.id)

    def test_str_representation(self):
        expected_str = (
            f"{self.sage_x3_transaction_info.transaction.transaction_id} - {self.sage_x3_transaction_info.status}"
        )
        self.assertEqual(str(self.sage_x3_transaction_info), expected_str)

    def test_retries_default_value(self):
        self.assertEqual(self.sage_x3_transaction_info.retries, 0)

    def test_status_can_be_blank(self):
        self.sage_x3_transaction_info.status = ""
        self.sage_x3_transaction_info.save()
        retrieved_info = SageX3TransactionInformation.objects.get(id=self.sage_x3_transaction_info.id)
        self.assertEqual(retrieved_info.status, "")

    def test_input_xml_can_be_blank(self):
        self.sage_x3_transaction_info.input_xml = ""
        self.sage_x3_transaction_info.save()
        retrieved_info = SageX3TransactionInformation.objects.get(id=self.sage_x3_transaction_info.id)
        self.assertEqual(retrieved_info.input_xml, "")

    def test_output_xml_can_be_blank(self):
        self.sage_x3_transaction_info.output_xml = ""
        self.sage_x3_transaction_info.save()
        retrieved_info = SageX3TransactionInformation.objects.get(id=self.sage_x3_transaction_info.id)
        self.assertEqual(retrieved_info.output_xml, "")
