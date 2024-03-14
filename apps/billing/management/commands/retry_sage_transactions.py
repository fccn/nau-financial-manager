import time

from django.core.management.base import BaseCommand

from apps.billing.models import SageX3TransactionInformation
from apps.billing.services.transaction_service import TransactionService


class Command(BaseCommand):
    """

    This command triggers allows to retry the failed Sage X3 transactions or
    forcelly send a specific transaction and optionally use a different series.

    How to use:

        python manage.py retry_sage_transactions

        python manage.py retry_sage_transactions --transaction_id=XXXX

    """

    help = "This command will collect all transactions failed and retry to send to sage X3"

    def add_arguments(self, parser):
        """
        Add command line arguments to this Django Command.
        """
        parser.add_argument(
            "--transaction_id", type=str, required=False, help="The transaction_id to retry to send to SageX3"
        )

    @staticmethod
    def _sagex3_transaction_info_query(transaction_id):
        if transaction_id:
            return SageX3TransactionInformation.objects.filter(transaction__transaction_id=transaction_id)
        else:
            return SageX3TransactionInformation.objects.filter(
                status__in=[SageX3TransactionInformation.FAILED, SageX3TransactionInformation.PENDING]
            )

    def handle(self, *args, **kwargs) -> str | None:
        transaction_id = kwargs["transaction_id"]
        start = time.time()
        self.stdout.write("\nGetting failed transactions with Sage X3...\n")
        sagex3_to_retry = self.__class__._sagex3_transaction_info_query(transaction_id)
        total_count = sagex3_to_retry.count()
        counters = {"success": 0, "failed": 0}
        try:
            for sagex3_failed_transaction in sagex3_to_retry:
                if TransactionService(sagex3_failed_transaction.transaction).run_steps_to_send_transaction():
                    counters["success"] += 1
                else:
                    counters["failed"] += 1
        except Exception as e:
            self.stdout.write(f"Error while retrying: {e}")
            counters["failed"] += 1
        finish = time.time() - start
        self.stdout.write(f"\n----- {total_count} Transactions were retried -----\n")
        self.stdout.write(f"\nSUCCESSFULL RETRIES: {counters['success']} FAILED RETRIES: {counters['failed']}\n")
        self.stdout.write(f"\nThe time to retry all transactions was {finish}\n")
