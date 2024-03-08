from unittest import mock

from django.test import override_settings
from django.test.testcases import TestCase
from requests.exceptions import Timeout

from apps.billing.factories import TransactionFactory, TransactionItemFactory
from apps.billing.models import SageX3TransactionInformation
from apps.billing.services.transaction_service import TransactionService
from apps.billing.tests.test_utils import processor_duplicate_error_response, processor_success_response


def raise_timeout(*args, **kwargs):
    raise Timeout("A testing exception has been raised")


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
        document_id: str = transaction.document_id

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
        document_id: str = transaction.document_id

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
        If an error is being raised during the communication with the processor then:
        - the document_id shouldn't be defined
        - status of the information should be failed
        Then some messages should be on the log and also on the output_xml field of the
        `SageX3TransactionInformation` object for that transaction.
        - A specific message should have been added to the log
        - The exception msg should be on the log
        - The name of the exception should be on the log
        """
        transaction = TransactionFactory.create()
        transaction.document_id = None
        transaction.save()
        transaction_service = TransactionService(transaction=transaction)

        with self.assertLogs(logger="apps.billing.services.transaction_service", level="ERROR") as cm:
            transaction_service.run_steps_to_send_transaction()

        transaction.refresh_from_db()

        self.assertEqual(transaction.document_id, None)
        self.assertEqual(transaction.sage_x3_transaction_information.status, SageX3TransactionInformation.FAILED)

        config = [
            {
                "to_check": "An exception has been raised when sending data to processor",
                "assert_msg": "A specific message should have been added to the ",
            },
            {"to_check": "A testing exception has been raised", "assert_msg": "The exception msg should be on the "},
            {"to_check": "Timeout", "assert_msg": "The name of the exception should be on the "},
        ]

        for snippet_to_check_in_log in config:
            for m in cm.output:
                self.assertIn(
                    snippet_to_check_in_log["to_check"],
                    m,
                    msg=snippet_to_check_in_log["assert_msg"] + "log",
                )

        output_xml = transaction.sage_x3_transaction_information.output_xml
        print(transaction.sage_x3_transaction_information.__dict__)
        for c in config:
            self.assertIn(
                c["to_check"],
                output_xml,
                msg=c["assert_msg"] + "output_xml",
            )
