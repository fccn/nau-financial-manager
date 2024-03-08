from unittest import mock

from django.test import override_settings
from django.test.testcases import TestCase
from requests.exceptions import Timeout

from apps.billing.factories import TransactionFactory, TransactionItemFactory
from apps.billing.models import SageX3TransactionInformation
from apps.billing.services.transaction_service import TransactionService
from apps.billing.tests.test_utils import processor_duplicate_error_response, processor_success_response


def raise_timeout(*args, **kwargs):
    raise Timeout("Test")

class TransactionServiceTestCase(TestCase):
    """
    Tests the `TransactionService`
    """

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com")
    @mock.patch("requests.post", side_effect=processor_success_response)
    def test_transaction_to_processor_success(self, mocked_post):
        """
        This test ensures the success result from the processor.

        Calling the `run_steps_to_send_transaction`, it deals with the success result
        and extracts the document id from response payload.
        """
        transaction = TransactionFactory.create()
        TransactionItemFactory.create(transaction=transaction)
        transaction_service = TransactionService(transaction=transaction)
        transaction_service.run_steps_to_send_transaction()
        document_id : str = transaction.document_id

        self.assertTrue(isinstance(document_id, str))
        self.assertNotEqual(document_id, "")
        self.assertTrue(document_id.startswith("FRN-"))

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com")
    @mock.patch("requests.post", side_effect=processor_duplicate_error_response)
    def test_transaction_to_processor_duplicate_error(self, mocked_post):
        """
        This test ensures the duplicate result from the processor.

        Calling the `run_steps_to_send_transaction`, it deals with the duplicate result
        and extracts the document id from response payload that indicates the duplicate information.
        """
        transaction = TransactionFactory.create()
        transaction_service = TransactionService(transaction=transaction)
        transaction_service.run_steps_to_send_transaction()
        document_id : str = transaction.document_id

        self.assertTrue(isinstance(document_id, str))
        self.assertNotEqual(document_id, "")
        self.assertTrue(document_id.startswith("FRN-"))

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com")
    @mock.patch("requests.post", side_effect=processor_success_response)
    def test_run_steps_to_send_transaction(self, mocked_post):
        """
        This test ensures the success triggering the method that runs each step to send a
        transaction to processor.
        """
        transaction = TransactionFactory.create()
        TransactionItemFactory.create(transaction=transaction)
        transaction_service = TransactionService(transaction=transaction)
        transaction_service.run_steps_to_send_transaction()

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com")
    @mock.patch("requests.post", side_effect=raise_timeout)
    def test_transaction_to_processor_timeout_error(self, mocked_post):
        """
        This test ensures that the transaction service correctly handles a timeout error from the processor.
        """
        transaction = TransactionFactory.create()
        transaction.document_id = None
        transaction_service = TransactionService(transaction=transaction)
        transaction_service.run_steps_to_send_transaction()
        document_id : str = transaction.document_id

        transaction.refresh_from_db()

        self.assertIsNone(document_id)
        self.assertEqual(transaction.sage_x3_transaction_information.status, SageX3TransactionInformation.FAILED)
