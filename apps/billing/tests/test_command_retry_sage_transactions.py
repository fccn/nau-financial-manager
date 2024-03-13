from unittest import mock

from django.core.management import call_command
from django.test import TestCase

from apps.billing.factories import SageX3TransactionInformationFactory, TransactionFactory, TransactionItemFactory
from apps.billing.models import SageX3TransactionInformation


def create_transaction(status):
    transaction = TransactionFactory.build()
    transaction.save()
    item = TransactionItemFactory.build(transaction=transaction)
    item.save()
    sageX3TI = SageX3TransactionInformationFactory.build(transaction=transaction, status=status)
    sageX3TI.save()
    return transaction


@mock.patch("apps.billing.services.transaction_service.TransactionService", autospec=True)
class CommandRetrySageTransactionsTestCase(TestCase):
    """
    Test the `retry_sage_transactions` Django command.
    """

    def test_command_retry_sage_transactions(self, transaction_service_mock):
        """
        Test the command `retry_sage_transactions`.
        Unfortunately all this calls needs to be on the same test.
        """
        call_command("retry_sage_transactions")
        transaction_service_mock.assert_not_called()

        # test a pending transaction should be retried
        t = create_transaction(SageX3TransactionInformation.PENDING)
        for _ in range(5):
            create_transaction(SageX3TransactionInformation.SUCCESS)
        call_command("retry_sage_transactions")
        transaction_service_mock.assert_called_once_with(t)

        # test a failed transaction should be retried
        f = create_transaction(SageX3TransactionInformation.FAILED)
        call_command("retry_sage_transactions")
        transaction_service_mock.assert_called_with(f)

        # test a failed transaction with a custom series should be retried
        t = create_transaction(SageX3TransactionInformation.FAILED)
        call_command("retry_sage_transactions", transaction_id=t.transaction_id, custom_series="KSERIES")
        transaction_service_mock.assert_called_with(t, series="KSERIES")

        # test the force retry of a success transaction
        t = create_transaction(SageX3TransactionInformation.SUCCESS)
        call_command("retry_sage_transactions", transaction_id=t.transaction_id)
        transaction_service_mock.assert_called_with(t)
