from unittest import mock

from django.test import override_settings
from django.test.testcases import TestCase
from requests.exceptions import Timeout

from apps.billing.factories import SageX3TransactionInformationFactory, TransactionFactory, TransactionItemFactory
from apps.billing.mocks import MockResponse
from apps.billing.models import SageX3TransactionInformation
from apps.billing.services.transaction_service import TransactionService
from apps.billing.tests.test_utils import processor_duplicate_error_response, processor_success_response


def raise_timeout(*args, **kwargs):
    raise Timeout("A testing exception has been raised")


class TransactionServiceTestCase(TestCase):
    """
    Tests the `TransactionService`
    """

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com", DEFAULT_SERIES="AAA")
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
        self.assertTrue(document_id.startswith("AAA-"))

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com", DEFAULT_SERIES="QWERTY")
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
        print(document_id)
        self.assertTrue(document_id.startswith("QWERTY-"))

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

        self.assertEqual(transaction.sage_x3_transaction_information.status, SageX3TransactionInformation.SUCCESS)

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com")
    @mock.patch("requests.post", side_effect=raise_timeout)
    def test_transaction_to_processor_timeout_error_log(self, mocked_post):
        """
        This test ensures that the transaction service correctly handles a timeout error from the processor.
        If an error is being raised during the communication with the processor then:
        - the document_id shouldn't be defined
        - status of the information should be failed
        Then some messages should be on the log:
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

        self.assertGreaterEqual(
            len(cm.output), 1, msg="At least a logging message should have been added with an error"
        )
        log_message = cm.output[0]
        self.assertIn(
            "An exception has been raised when sending data to processor",
            log_message,
            msg="A specific message should have been added to the log",
        )
        self.assertIn(
            "A testing exception has been raised",
            log_message,
            msg="The exception msg should be on the log",
        )
        self.assertIn(
            "Timeout",
            log_message,
            msg="The name of the exception should be on the log",
        )

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com")
    @mock.patch("requests.post", side_effect=raise_timeout)
    def test_transaction_to_processor_timeout_error_messages(self, mocked_post):
        """
        This test ensures that the transaction service correctly handles a timeout error from the processor.
        If an error is being raised during the communication with the processor then:
        - the document_id shouldn't be defined
        - status of the information should be failed
        Then the error_messages field of the `SageX3TransactionInformation` object for that transaction should contain:
        - A specific message
        - The exception msg
        - The name of the exception
        """
        transaction = TransactionFactory.create()
        transaction.document_id = None
        transaction.save()
        transaction_service = TransactionService(transaction=transaction)
        transaction_service.run_steps_to_send_transaction()

        transaction.refresh_from_db()
        self.assertEqual(transaction.document_id, None)
        self.assertEqual(transaction.sage_x3_transaction_information.status, SageX3TransactionInformation.FAILED)
        self.assertEqual(transaction.sage_x3_transaction_information.retries, 1)

        error_messages = transaction.sage_x3_transaction_information.error_messages
        self.assertIn(
            "An exception has been raised when sending data to processor",
            error_messages,
            msg="A specific message should have been added to the error_messages",
        )
        self.assertIn(
            "A testing exception has been raised",
            error_messages,
            msg="The exception msg should be on the error_messages",
        )
        self.assertIn(
            "Timeout",
            error_messages,
            msg="The name of the exception should be on the error_messages",
        )

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com")
    @mock.patch("requests.post", side_effect=raise_timeout)
    def test_transaction_to_processor_error_retries_increase(self, mocked_post):
        """
        This test ensures that the retries flag increase when some error occurs when sending
        transaction through the processor.
        """
        transaction = TransactionFactory.create()
        transaction.document_id = None
        transaction.save()
        transaction_service = TransactionService(transaction=transaction)

        transaction_service.run_steps_to_send_transaction()
        transaction_service.run_steps_to_send_transaction()
        transaction_service.run_steps_to_send_transaction()

        transaction.refresh_from_db()
        self.assertEqual(transaction.sage_x3_transaction_information.retries, 3)

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com")
    @mock.patch("requests.post", side_effect=raise_timeout)
    def test_transaction_to_processor_error_with_input_xml(self, mocked_post):
        """
        This test ensures that in case of error sending to processor we still have the input_xml value.
        """
        transaction = TransactionFactory.create()
        transaction.document_id = None
        transaction.save()
        transaction_service = TransactionService(transaction=transaction)

        transaction_service.run_steps_to_send_transaction()
        transaction.refresh_from_db()

        self.assertEqual(transaction.document_id, None)
        self.assertTrue("<soapenv:Envelope" in transaction.sage_x3_transaction_information.input_xml)
        self.assertEqual(transaction.sage_x3_transaction_information.retries, 1)

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com")
    @mock.patch("requests.post", return_value=MockResponse(status_code=500, data="Some not expected error"))
    def test_transaction_to_processor_not_expected_error(self, mocked_post):
        """
        This test ensures the success triggering the method that runs each step to send a
        transaction to processor.
        """
        transaction = TransactionFactory.create()
        TransactionItemFactory.create(transaction=transaction)
        transaction_service = TransactionService(transaction=transaction)
        transaction_service.run_steps_to_send_transaction()

        self.assertEqual(transaction.sage_x3_transaction_information.status, SageX3TransactionInformation.FAILED)
        self.assertIn("Some not expected error", transaction.sage_x3_transaction_information.output_xml)
        self.assertIn(
            "An exception has been raised when sending data to processor",
            transaction.sage_x3_transaction_information.error_messages,
        )

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com")
    @mock.patch("requests.post", side_effect=processor_success_response)
    def test_transaction_to_processor_log_xml(self, mocked_post):
        """
        This test ensures that the data input xml and output xml is logged.
        """
        transaction = TransactionFactory.create()
        TransactionItemFactory.create(transaction=transaction)
        transaction_service = TransactionService(transaction=transaction)

        with self.assertLogs(logger="apps.billing.services.transaction_service", level="INFO") as cm:
            transaction_service.run_steps_to_send_transaction()

        transaction.refresh_from_db()

        self.assertGreaterEqual(len(cm.output), 1)
        log_message_input = cm.output[0]
        self.assertIn("Send transaction to SageX3 input_xml", log_message_input)
        self.assertIn("<soapenv:Envelope", log_message_input)

        self.assertGreaterEqual(len(cm.output), 2)
        log_message_output = cm.output[1]
        self.assertIn("Receiving from SageX3 the response", log_message_output)
        self.assertIn("<soapenv:Envelope", log_message_output)

    def test_sagex3_transaction_info_query_with_transaction_id_FAILED_status(self):
        """
        This test validates the query providing the `transaction_id` of a transaction
        with `FAILED` status
        """

        transaction = TransactionFactory.create()

        SageX3TransactionInformationFactory.create(transaction=transaction, status=SageX3TransactionInformation.FAILED)

        transaction_information: list[SageX3TransactionInformation] = TransactionService.sagex3_transaction_info_query(
            transaction.transaction_id
        )

        self.assertTrue(isinstance(transaction_information, list))
        self.assertEqual(len(transaction_information), 1)
        self.assertEqual(transaction_information[0].transaction.transaction_id, transaction.transaction_id)
        self.assertEqual(transaction_information[0].status, SageX3TransactionInformation.FAILED)

    def test_sagex3_transaction_info_query_with_transaction_id_PENDING(self):
        """
        This test validates the query providing the `transaction_id` of a transaction
        with `PENDIND` status
        """

        transaction = TransactionFactory.create()

        SageX3TransactionInformationFactory.create(
            transaction=transaction, status=SageX3TransactionInformation.PENDING
        )

        transaction_information: list[SageX3TransactionInformation] = TransactionService.sagex3_transaction_info_query(
            transaction.transaction_id
        )

        self.assertTrue(isinstance(transaction_information, list))
        self.assertEqual(len(transaction_information), 1)
        self.assertEqual(transaction_information[0].transaction.transaction_id, transaction.transaction_id)
        self.assertEqual(transaction_information[0].status, SageX3TransactionInformation.PENDING)

    def test_sagex3_transaction_info_query_wrong_transaction_id(self):
        """
        This test validates the query providing a `transaction_id` that does not exist
        """

        transaction = TransactionFactory.create()

        SageX3TransactionInformationFactory.create(transaction=transaction, status=SageX3TransactionInformation.FAILED)

        transaction_information: list[SageX3TransactionInformation] = TransactionService.sagex3_transaction_info_query(
            "TRANSACTION_ID"
        )

        self.assertTrue(isinstance(transaction_information, list))
        self.assertEqual(len(transaction_information), 0)

    def test_sagex3_transaction_info_query_without_transaction_id(self):
        """
        This test validates the query without providing a `transaction_id`
        """

        for transaction in TransactionFactory.create_batch(10):
            SageX3TransactionInformationFactory.create(
                transaction=transaction, status=SageX3TransactionInformation.FAILED
            )

        for transaction in TransactionFactory.create_batch(10):
            SageX3TransactionInformationFactory.create(
                transaction=transaction, status=SageX3TransactionInformation.PENDING
            )

        transactions_information: list[
            SageX3TransactionInformation
        ] = TransactionService.sagex3_transaction_info_query(transaction_id=None)

        self.assertTrue(isinstance(transactions_information, list))
        self.assertEqual(len(transactions_information), 20)

        failed_transactions = [
            transaction
            for transaction in transactions_information
            if transaction.status == SageX3TransactionInformation.FAILED
        ]

        pending_transactions = [
            transaction
            for transaction in transactions_information
            if transaction.status == SageX3TransactionInformation.PENDING
        ]

        self.assertEqual(len(failed_transactions), 10)
        self.assertEqual(len(pending_transactions), 10)

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com", DEFAULT_SERIES="AAA")
    @mock.patch("requests.post", side_effect=processor_success_response)
    def test_retry_transaction_to_processor_success_FAILED_status(self, mocked_post):
        """
        This test validates retry sending transaction resources of a transaction
        with `FAILED` status
        """

        transaction = TransactionFactory.create()
        TransactionItemFactory.create(transaction=transaction)

        SageX3TransactionInformationFactory.create(transaction=transaction, status=SageX3TransactionInformation.FAILED)

        transaction_information: list[SageX3TransactionInformation] = TransactionService.sagex3_transaction_info_query(
            transaction.transaction_id
        )

        counters = TransactionService.retry_sending_transactions(transaction_id=transaction.transaction_id)

        self.assertTrue(isinstance(transaction_information, list))
        self.assertEqual(len(transaction_information), 1)
        self.assertEqual(transaction_information[0].transaction.transaction_id, transaction.transaction_id)
        self.assertEqual(transaction_information[0].status, SageX3TransactionInformation.FAILED)

        self.assertTrue(isinstance(counters, dict))
        self.assertEqual(counters["total_count"], 1)
        self.assertEqual(counters["success"], 1)
        self.assertEqual(counters["failed"], 0)

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com", DEFAULT_SERIES="AAA")
    @mock.patch("requests.post", side_effect=processor_success_response)
    def test_retry_transaction_to_processor_success_PENDING_status(self, mocked_post):
        """
        This test validates retry sending transaction resources of a transaction
        with `PENDING` status
        """

        transaction = TransactionFactory.create()
        TransactionItemFactory.create(transaction=transaction)

        SageX3TransactionInformationFactory.create(
            transaction=transaction, status=SageX3TransactionInformation.PENDING
        )

        transaction_information: list[SageX3TransactionInformation] = TransactionService.sagex3_transaction_info_query(
            transaction.transaction_id
        )

        counters = TransactionService.retry_sending_transactions(transaction_id=transaction.transaction_id)

        self.assertTrue(isinstance(transaction_information, list))
        self.assertEqual(len(transaction_information), 1)
        self.assertEqual(transaction_information[0].transaction.transaction_id, transaction.transaction_id)
        self.assertEqual(transaction_information[0].status, SageX3TransactionInformation.PENDING)

        self.assertTrue(isinstance(counters, dict))
        self.assertEqual(counters["total_count"], 1)
        self.assertEqual(counters["success"], 1)
        self.assertEqual(counters["failed"], 0)

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com", DEFAULT_SERIES="AAA")
    @mock.patch("requests.post", side_effect=processor_duplicate_error_response)
    def test_retry_transaction_to_processor_duplicate_error_response(self, mocked_post):
        """
        This test validates retry sending transaction resources when the respose is
        a duplicate error response
        """

        transaction = TransactionFactory.create()
        TransactionItemFactory.create(transaction=transaction)

        SageX3TransactionInformationFactory.create(transaction=transaction, status=SageX3TransactionInformation.FAILED)

        transaction_information: list[SageX3TransactionInformation] = TransactionService.sagex3_transaction_info_query(
            transaction.transaction_id
        )

        counters = TransactionService.retry_sending_transactions(transaction_id=transaction.transaction_id)

        self.assertTrue(isinstance(transaction_information, list))
        self.assertEqual(len(transaction_information), 1)
        self.assertEqual(transaction_information[0].transaction.transaction_id, transaction.transaction_id)
        self.assertEqual(transaction_information[0].status, SageX3TransactionInformation.FAILED)

        self.assertTrue(isinstance(counters, dict))
        self.assertEqual(counters["total_count"], 1)
        self.assertEqual(counters["success"], 1)
        self.assertEqual(counters["failed"], 0)

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com", DEFAULT_SERIES="AAA")
    @mock.patch("requests.post", side_effect=processor_success_response)
    def test_retry_transaction_to_processor_success_without_transaction_id(self, mocked_post):
        """
        This test validates retry sending transaction resources without providing a `transaction_id`
        """

        for transaction in TransactionFactory.create_batch(10):
            TransactionItemFactory.create(transaction=transaction)
            SageX3TransactionInformationFactory.create(
                transaction=transaction, status=SageX3TransactionInformation.FAILED
            )

        for transaction in TransactionFactory.create_batch(10):
            TransactionItemFactory.create(transaction=transaction)
            SageX3TransactionInformationFactory.create(
                transaction=transaction, status=SageX3TransactionInformation.PENDING
            )

        transactions_information: list[
            SageX3TransactionInformation
        ] = TransactionService.sagex3_transaction_info_query(transaction_id=None)

        self.assertTrue(isinstance(transactions_information, list))
        self.assertEqual(len(transactions_information), 20)

        failed_transactions = [
            transaction
            for transaction in transactions_information
            if transaction.status == SageX3TransactionInformation.FAILED
        ]

        pending_transactions = [
            transaction
            for transaction in transactions_information
            if transaction.status == SageX3TransactionInformation.PENDING
        ]

        self.assertEqual(len(failed_transactions), 10)
        self.assertEqual(len(pending_transactions), 10)

        counters = TransactionService.retry_sending_transactions(transaction_id=None)

        self.assertTrue(isinstance(counters, dict))
        self.assertEqual(counters["total_count"], 20)
        self.assertEqual(counters["success"], 20)
        self.assertEqual(counters["failed"], 0)

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com")
    @mock.patch("requests.post", return_value=MockResponse(status_code=500, data="Some not expected error"))
    def test_retry_transaction_to_processor_error_PENDING_status(self, mocked_post):
        """
        This test validates retry sending transaction resources of a transaction
        with `PENDING` status receiving an internal server response from `SageX3`
        """

        transaction = TransactionFactory.create()
        TransactionItemFactory.create(transaction=transaction)

        SageX3TransactionInformationFactory.create(
            transaction=transaction, status=SageX3TransactionInformation.PENDING
        )

        transaction_information: list[SageX3TransactionInformation] = TransactionService.sagex3_transaction_info_query(
            transaction.transaction_id
        )

        counters = TransactionService.retry_sending_transactions(transaction_id=transaction.transaction_id)

        self.assertTrue(isinstance(transaction_information, list))
        self.assertEqual(len(transaction_information), 1)
        self.assertEqual(transaction_information[0].transaction.transaction_id, transaction.transaction_id)
        self.assertEqual(transaction_information[0].status, SageX3TransactionInformation.PENDING)

        self.assertTrue(isinstance(counters, dict))
        self.assertEqual(counters["total_count"], 1)
        self.assertEqual(counters["success"], 0)
        self.assertEqual(counters["failed"], 1)

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com")
    @mock.patch("requests.post", return_value=MockResponse(status_code=500, data="Some not expected error"))
    def test_retry_transaction_to_processor_error_FAILED_status(self, mocked_post):
        """
        This test validates retry sending transaction resources of a transaction
        with `FAILED` status receiving an internal server response from `SageX3`
        """

        transaction = TransactionFactory.create()
        TransactionItemFactory.create(transaction=transaction)

        SageX3TransactionInformationFactory.create(transaction=transaction, status=SageX3TransactionInformation.FAILED)

        transaction_information: list[SageX3TransactionInformation] = TransactionService.sagex3_transaction_info_query(
            transaction.transaction_id
        )

        counters = TransactionService.retry_sending_transactions(transaction_id=transaction.transaction_id)

        self.assertTrue(isinstance(transaction_information, list))
        self.assertEqual(len(transaction_information), 1)
        self.assertEqual(transaction_information[0].transaction.transaction_id, transaction.transaction_id)
        self.assertEqual(transaction_information[0].status, SageX3TransactionInformation.FAILED)

        self.assertTrue(isinstance(counters, dict))
        self.assertEqual(counters["total_count"], 1)
        self.assertEqual(counters["success"], 0)
        self.assertEqual(counters["failed"], 1)

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com")
    @mock.patch("requests.post", return_value=MockResponse(status_code=500, data="Some not expected error"))
    def test_retry_transaction_to_processor_error_without_transaction_id(self, mocked_post):
        """
        This test validates retry sending transaction resources without providing a `transaction_id`
        receiving an internal server response from `SageX3`
        """

        for transaction in TransactionFactory.create_batch(10):
            TransactionItemFactory.create(transaction=transaction)
            SageX3TransactionInformationFactory.create(
                transaction=transaction, status=SageX3TransactionInformation.FAILED
            )

        for transaction in TransactionFactory.create_batch(10):
            TransactionItemFactory.create(transaction=transaction)
            SageX3TransactionInformationFactory.create(
                transaction=transaction, status=SageX3TransactionInformation.PENDING
            )

        transactions_information: list[
            SageX3TransactionInformation
        ] = TransactionService.sagex3_transaction_info_query(transaction_id=None)

        self.assertTrue(isinstance(transactions_information, list))
        self.assertEqual(len(transactions_information), 20)

        failed_transactions = [
            transaction
            for transaction in transactions_information
            if transaction.status == SageX3TransactionInformation.FAILED
        ]

        pending_transactions = [
            transaction
            for transaction in transactions_information
            if transaction.status == SageX3TransactionInformation.PENDING
        ]

        self.assertEqual(len(failed_transactions), 10)
        self.assertEqual(len(pending_transactions), 10)

        counters = TransactionService.retry_sending_transactions(transaction_id=None)

        self.assertTrue(isinstance(counters, dict))
        self.assertEqual(counters["total_count"], 20)
        self.assertEqual(counters["success"], 0)
        self.assertEqual(counters["failed"], 20)

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com", DEFAULT_SERIES="AAA")
    @mock.patch("requests.post", side_effect=processor_success_response)
    def test_retry_transaction_to_processor_no_transactions(self, mocked_post):
        """
        This test validates retry sending transaction resources without transactions
        """

        counters = TransactionService.retry_sending_transactions(transaction_id=None)

        self.assertTrue(isinstance(counters, dict))
        self.assertEqual(counters["total_count"], 0)
        self.assertEqual(counters["success"], 0)
        self.assertEqual(counters["failed"], 0)

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com")
    @mock.patch("requests.post", side_effect=raise_timeout)
    def test_retry_transaction_to_processor_timeout_FAILED_status(self, mocked_post):
        """
        This test validates retry sending transaction resources of a transaction
        with `FAILED` status receiving a timeout error response from `SageX3`
        """

        transaction = TransactionFactory.create()
        TransactionItemFactory.create(transaction=transaction)

        SageX3TransactionInformationFactory.create(transaction=transaction, status=SageX3TransactionInformation.FAILED)

        transaction_information: list[SageX3TransactionInformation] = TransactionService.sagex3_transaction_info_query(
            transaction.transaction_id
        )

        counters = TransactionService.retry_sending_transactions(transaction_id=transaction.transaction_id)

        self.assertTrue(isinstance(transaction_information, list))
        self.assertEqual(len(transaction_information), 1)
        self.assertEqual(transaction_information[0].transaction.transaction_id, transaction.transaction_id)
        self.assertEqual(transaction_information[0].status, SageX3TransactionInformation.FAILED)

        self.assertTrue(isinstance(counters, dict))
        self.assertEqual(counters["total_count"], 1)
        self.assertEqual(counters["success"], 0)
        self.assertEqual(counters["failed"], 1)

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com")
    @mock.patch("requests.post", side_effect=raise_timeout)
    def test_retry_transaction_to_processor_timeout_PENDIND_status(self, mocked_post):
        """
        This test validates retry sending transaction resources of a transaction
        with `PENDIND` status receiving a timeout error response from `SageX3`
        """

        transaction = TransactionFactory.create()
        TransactionItemFactory.create(transaction=transaction)

        SageX3TransactionInformationFactory.create(
            transaction=transaction, status=SageX3TransactionInformation.PENDING
        )

        transaction_information: list[SageX3TransactionInformation] = TransactionService.sagex3_transaction_info_query(
            transaction.transaction_id
        )

        counters = TransactionService.retry_sending_transactions(transaction_id=transaction.transaction_id)

        self.assertTrue(isinstance(transaction_information, list))
        self.assertEqual(len(transaction_information), 1)
        self.assertEqual(transaction_information[0].transaction.transaction_id, transaction.transaction_id)
        self.assertEqual(transaction_information[0].status, SageX3TransactionInformation.PENDING)

        self.assertTrue(isinstance(counters, dict))
        self.assertEqual(counters["total_count"], 1)
        self.assertEqual(counters["success"], 0)
        self.assertEqual(counters["failed"], 1)
