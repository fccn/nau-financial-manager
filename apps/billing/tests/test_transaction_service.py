from unittest import mock

from django.conf import settings
from django.test.testcases import TestCase
from requests.exceptions import Timeout

from apps.billing.factories import TransactionFactory, TransactionItemFactory
from apps.billing.services.financial_processor_service import TransactionProcessorInterface
from apps.billing.services.transaction_service import TransactionService
from apps.billing.tests.test_utils import processor_duplicate_error_response, processor_success_response


class TransactionServiceTestCase(TestCase):
    def setUp(self) -> None:
        """
        This method instantiates all the necessary components, get the url for transaction processor service
        and creates a combination of one `Transaction` and `TransactionItem`.
        """

        self.transaction = TransactionFactory.create()
        self.transaction_item = TransactionItemFactory.create(transaction=self.transaction)
        self.processor_url = getattr(settings, "TRANSACTION_PROCESSOR_URL")
        self.transaction_service = TransactionService(transaction=self.transaction)

    def test_financial_processor_service_interface(self):
        """
        This test ensures that if not implemented, the method from the interface
        will raise an exception.

        """
        with self.assertRaisesMessage(
            expected_exception=Exception,
            expected_message="This method needs to be implemented",
        ):
            TransactionProcessorInterface(None).send_transaction_to_processor()

    @mock.patch("requests.post", side_effect=processor_success_response)
    def test_transaction_to_processor_success(self, mocked_post):
        """
        This test ensures the success result from the processor.

        Calling the `self.transaction_service.send_transaction_to_processor`, it deals with the success result
        and extracts the document id from response payload.
        """

        fake_url_processor = "http://fake-processor.com"
        setattr(settings, "TRANSACTION_PROCESSOR_URL", fake_url_processor)

        document_id: str = self.transaction_service.send_transaction_to_processor()

        self.assertTrue(isinstance(document_id, str))
        self.assertNotEqual(document_id, "")
        self.assertTrue(document_id.startswith("FRN-"))

    @mock.patch("requests.post", side_effect=processor_duplicate_error_response)
    def test_transaction_to_processor_duplicate_error(self, mocked_post):
        """
        This test ensures the duplicate result from the processor.

        Calling the `self.transaction_service.send_transaction_to_processor`, it deals with the duplicate result
        and extracts the document id from response payload that indicates the duplicate information.
        """

        fake_url_processor = "http://fake-processor.com"
        setattr(settings, "TRANSACTION_PROCESSOR_URL", fake_url_processor)

        document_id: str = self.transaction_service.send_transaction_to_processor()

        self.assertTrue(isinstance(document_id, str))
        self.assertNotEqual(document_id, "")
        self.assertTrue(document_id.startswith("FRN-"))

    @mock.patch("requests.post", side_effect=processor_success_response)
    def test_run_steps_to_send_transaction(self, mocked_post):
        """
        This test ensures the success triggering the method that runs each step to send a
        transaction to processor.
        """

        fake_url_processor = "http://fake-processor.com"
        setattr(settings, "TRANSACTION_PROCESSOR_URL", fake_url_processor)

        self.transaction_service.run_steps_to_send_transaction()

    @mock.patch("requests.post", side_effect=Timeout)
    def test_transaction_to_processor_timeout_error(self, mocked_post):
        """
        This test ensures that the transaction service correctly handles a timeout error from the processor.
        """

        fake_url_processor = "http://fake-processor.com"
        setattr(settings, "TRANSACTION_PROCESSOR_URL", fake_url_processor)

        with self.assertRaises(Timeout):
            self.transaction_service.send_transaction_to_processor()

    def tearDown(self) -> None:
        """
        This method is called in the last moment of the `TestCase` class and sets the `TRANSACTION_PROCESSOR_URL`
        varible as the real service url again.
        """
        setattr(settings, "TRANSACTION_PROCESSOR_URL", self.processor_url)
