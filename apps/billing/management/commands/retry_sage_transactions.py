import time

from django.core.management.base import BaseCommand

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

    def handle(self, *args, **kwargs) -> str | None:
        transaction_id = kwargs["transaction_id"]
        start = time.time()
        self.stdout.write("\nGetting failed transactions with Sage X3...\n")
        counters = TransactionService.retry_sending_transactions(transaction_id=transaction_id)
        finish = time.time() - start
        self.stdout.write(f"\n----- {counters['total_count']} Transactions were retried -----\n")
        self.stdout.write(f"\nSUCCESSFULL RETRIES: {counters['success']} FAILED RETRIES: {counters['failed']}\n")
        self.stdout.write(f"\nThe time to retry all transactions was {finish}\n")
