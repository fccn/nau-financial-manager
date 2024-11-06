from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.test import TestCase, override_settings

from apps.billing.factories import SageX3TransactionInformationFactory, TransactionFactory, TransactionItemFactory
from apps.billing.mocks import MockResponse
from apps.billing.models import SageX3TransactionInformation
from apps.billing.tests.test_transaction_service import raise_timeout
from apps.billing.tests.test_utils import processor_duplicate_error_response, processor_success_response


class CommandRetrySageTransactionsTestCase(TestCase):
    """
    Test the `retry_sage_transactions` Django command.
    """

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com", DEFAULT_SERIES="AAA")
    @mock.patch("requests.post", side_effect=processor_success_response)
    def test_command_retry_sage_transactions_no_transactions(self, mocked_post):
        """
        This test ensures the custom command functionality with no transactions to retry.
        """

        out = StringIO()

        call_command("retry_sage_transactions", stdout=out)

        message = "----- 0 Transactions were retried -----\n\nSUCCESSFULL RETRIES: 0 FAILED RETRIES: 0"

        self.assertTrue(message in out.getvalue())

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com", DEFAULT_SERIES="AAA")
    @mock.patch("requests.post", side_effect=processor_success_response)
    def test_command_retry_sage_transactions_not_found_transaction(self, mocked_post):
        """
        This test ensures the custom command functionality with a not found `transaction_id`.
        """

        out = StringIO()

        call_command("retry_sage_transactions", "--transaction_id=WRONG_TRANSACTION_ID", stdout=out)

        message = "----- 0 Transactions were retried -----\n\nSUCCESSFULL RETRIES: 0 FAILED RETRIES: 0"

        self.assertTrue(message in out.getvalue())

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com", DEFAULT_SERIES="AAA")
    @mock.patch("requests.post", side_effect=processor_success_response)
    def test_command_retry_sage_transactions_success_PENDIND_status(self, mocked_post):
        """
        This test ensures the custom command functionality for a transaction with `PENDING` status.
        """

        out = StringIO()
        transaction = TransactionFactory.create()
        TransactionItemFactory.create(transaction=transaction)

        SageX3TransactionInformationFactory.create(
            transaction=transaction, status=SageX3TransactionInformation.PENDING
        )

        call_command("retry_sage_transactions", f"--transaction_id={transaction.transaction_id}", stdout=out)

        message = "----- 1 Transactions were retried -----\n\nSUCCESSFULL RETRIES: 1 FAILED RETRIES: 0"

        self.assertTrue(message in out.getvalue())

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com", DEFAULT_SERIES="AAA")
    @mock.patch("requests.post", side_effect=processor_success_response)
    def test_command_retry_sage_transactions_success_FAILED_status(self, mocked_post):
        """
        This test ensures the custom command functionality for a transaction with `FAILED` status.
        """

        out = StringIO()
        transaction = TransactionFactory.create()
        TransactionItemFactory.create(transaction=transaction)

        SageX3TransactionInformationFactory.create(transaction=transaction, status=SageX3TransactionInformation.FAILED)

        call_command("retry_sage_transactions", f"--transaction_id={transaction.transaction_id}", stdout=out)

        message = "----- 1 Transactions were retried -----\n\nSUCCESSFULL RETRIES: 1 FAILED RETRIES: 0"

        self.assertTrue(message in out.getvalue())

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com", DEFAULT_SERIES="AAA")
    @mock.patch("requests.post", side_effect=processor_success_response)
    def test_command_retry_sage_transactions_success_without_transaction_id(self, mocked_post):
        """
        This test ensures the custom command functionality without providing a `transaction_id`.
        """

        out = StringIO()

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

        call_command("retry_sage_transactions", stdout=out)

        message = "----- 20 Transactions were retried -----\n\nSUCCESSFULL RETRIES: 20 FAILED RETRIES: 0"

        self.assertTrue(message in out.getvalue())

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com", DEFAULT_SERIES="AAA")
    @mock.patch("requests.post", return_value=MockResponse(status_code=500, data="Some not expected error"))
    def test_command_retry_sage_transactions_error_PENDIND_status(self, mocked_post):
        """
        This test ensures the custom command functionality receiving an internal server error
        from `SageX3` retrying a transaction with `PENDING` status.
        """

        out = StringIO()
        transaction = TransactionFactory.create()
        TransactionItemFactory.create(transaction=transaction)

        SageX3TransactionInformationFactory.create(
            transaction=transaction, status=SageX3TransactionInformation.PENDING
        )

        call_command("retry_sage_transactions", f"--transaction_id={transaction.transaction_id}", stdout=out)

        message = "----- 1 Transactions were retried -----\n\nSUCCESSFULL RETRIES: 0 FAILED RETRIES: 1"

        self.assertTrue(message in out.getvalue())

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com", DEFAULT_SERIES="AAA")
    @mock.patch("requests.post", return_value=MockResponse(status_code=500, data="Some not expected error"))
    def test_command_retry_sage_transactions_error_FAILED_status(self, mocked_post):
        """
        This test ensures the custom command functionality receiving an internal server error
        from `SageX3` retrying a transaction with `FAILED` status.
        """

        out = StringIO()
        transaction = TransactionFactory.create()
        TransactionItemFactory.create(transaction=transaction)

        SageX3TransactionInformationFactory.create(transaction=transaction, status=SageX3TransactionInformation.FAILED)

        call_command("retry_sage_transactions", f"--transaction_id={transaction.transaction_id}", stdout=out)

        message = "----- 1 Transactions were retried -----\n\nSUCCESSFULL RETRIES: 0 FAILED RETRIES: 1"

        self.assertTrue(message in out.getvalue())

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com", DEFAULT_SERIES="AAA")
    @mock.patch("requests.post", return_value=MockResponse(status_code=500, data="Some not expected error"))
    def test_command_retry_sage_transactions_error_without_transaction_id(self, mocked_post):
        """
        This test ensures the custom command functionality receiving an internal server error
        from `SageX3` without providing a `transaction_id`.
        """

        out = StringIO()

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

        call_command("retry_sage_transactions", stdout=out)

        message = "----- 20 Transactions were retried -----\n\nSUCCESSFULL RETRIES: 0 FAILED RETRIES: 20"

        self.assertTrue(message in out.getvalue())

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com")
    @mock.patch("requests.post", side_effect=raise_timeout)
    def test_command_retry_sage_transactions_timeout_error_PENDIND_status(self, mocked_post):
        """
        This test ensures the custom command functionality receiving a timeout error
        from `SageX3` retrying a transaction with `PENDING` status.
        """

        out = StringIO()
        transaction = TransactionFactory.create()
        TransactionItemFactory.create(transaction=transaction)

        SageX3TransactionInformationFactory.create(
            transaction=transaction, status=SageX3TransactionInformation.PENDING
        )

        call_command("retry_sage_transactions", f"--transaction_id={transaction.transaction_id}", stdout=out)

        message = "----- 1 Transactions were retried -----\n\nSUCCESSFULL RETRIES: 0 FAILED RETRIES: 1"

        self.assertTrue(message in out.getvalue())

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com")
    @mock.patch("requests.post", side_effect=raise_timeout)
    def test_command_retry_sage_transactions_timeout_error_FAILED_status(self, mocked_post):
        """
        This test ensures the custom command functionality receiving a timeout error
        from `SageX3` retrying a transaction with `FAILED` status.
        """

        out = StringIO()
        transaction = TransactionFactory.create()
        TransactionItemFactory.create(transaction=transaction)

        SageX3TransactionInformationFactory.create(transaction=transaction, status=SageX3TransactionInformation.FAILED)

        call_command("retry_sage_transactions", f"--transaction_id={transaction.transaction_id}", stdout=out)

        message = "----- 1 Transactions were retried -----\n\nSUCCESSFULL RETRIES: 0 FAILED RETRIES: 1"

        self.assertTrue(message in out.getvalue())

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com")
    @mock.patch("requests.post", side_effect=raise_timeout)
    def test_command_retry_sage_transactions_timeout_error_without_transaction_id(self, mocked_post):
        """
        This test ensures the custom command functionality receiving a timeout error
        from `SageX3` without providing a `transaction_id`.
        """

        out = StringIO()

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

        call_command("retry_sage_transactions", stdout=out)

        message = "----- 20 Transactions were retried -----\n\nSUCCESSFULL RETRIES: 0 FAILED RETRIES: 20"

        self.assertTrue(message in out.getvalue())

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com", DEFAULT_SERIES="AAA")
    @mock.patch("requests.post", side_effect=processor_duplicate_error_response)
    def test_command_retry_sage_transactions_duplicate_error_PENDING_status(self, mocked_post):
        """
        This test ensures the custom command functionality receiving a duplicate error response
        for a transaction with `PENDING` status.
        """

        out = StringIO()
        transaction = TransactionFactory.create()
        TransactionItemFactory.create(transaction=transaction)

        SageX3TransactionInformationFactory.create(
            transaction=transaction, status=SageX3TransactionInformation.PENDING
        )

        call_command("retry_sage_transactions", f"--transaction_id={transaction.transaction_id}", stdout=out)

        message = "----- 1 Transactions were retried -----\n\nSUCCESSFULL RETRIES: 1 FAILED RETRIES: 0"

        self.assertTrue(message in out.getvalue())

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com", DEFAULT_SERIES="AAA")
    @mock.patch("requests.post", side_effect=processor_duplicate_error_response)
    def test_command_retry_sage_transactions_duplicate_error_FAILED_status(self, mocked_post):
        """
        This test ensures the custom command functionality receiving a duplicate error response
        for a transaction with `FAILED` status.
        """

        out = StringIO()
        transaction = TransactionFactory.create()
        TransactionItemFactory.create(transaction=transaction)

        SageX3TransactionInformationFactory.create(transaction=transaction, status=SageX3TransactionInformation.FAILED)

        call_command("retry_sage_transactions", f"--transaction_id={transaction.transaction_id}", stdout=out)

        message = "----- 1 Transactions were retried -----\n\nSUCCESSFULL RETRIES: 1 FAILED RETRIES: 0"

        self.assertTrue(message in out.getvalue())

    @override_settings(TRANSACTION_PROCESSOR_URL="http://fake-processor.com", DEFAULT_SERIES="AAA")
    @mock.patch("requests.post", side_effect=processor_duplicate_error_response)
    def test_command_retry_sage_transactions_duplicate_error(self, mocked_post):
        """
        This test ensures the custom command functionality receiving a duplicate error response
        without providing a `transaction_id`.
        """

        out = StringIO()

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

        call_command("retry_sage_transactions", stdout=out)

        message = "----- 20 Transactions were retried -----\n\nSUCCESSFULL RETRIES: 20 FAILED RETRIES: 0"

        self.assertTrue(message in out.getvalue())
