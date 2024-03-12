import time

from django.core.management.base import BaseCommand, CommandError

from apps.billing.models import SageX3TransactionInformation
from apps.billing.services.transaction_service import TransactionService


class Command(BaseCommand):
    """

    This command triggers the all sage X3 failed transactions.

    How to use:

        python manage.py retry_sage_transactions

    """

    help = "This command will collect all trasanctions failed and retry to send to sage X3"

    def handle(self, *args, **options) -> str | None:
        try:
            start = time.time()
            self.stdout.write("\nGetting failed transactions with Sage X3...\n")
            sagex3_failed_transactions = SageX3TransactionInformation.objects.filter(
                status__in=[SageX3TransactionInformation.FAILED, SageX3TransactionInformation.PENDING]
            )
            sagex3_failed_transactions_amount = sagex3_failed_transactions.count()
            counters = {"success": 0, "failed": 0}
            try:
                for sagex3_failed_transaction in sagex3_failed_transactions:
                    TransactionService(sagex3_failed_transaction.transaction).run_steps_to_send_transaction()
                    counters["success"] += 1
            except Exception as e:
                self.stdout.write(f"Error while retrying: {e}")
                counters["failed"] += 1
            finish = time.time() - start
            self.stdout.write(f"\n----- {sagex3_failed_transactions_amount} Transactions were retried -----\n")
            self.stdout.write(f"\nSUCCESSFULL RETRIES: {counters['success']} FAILED RETRIES: {counters['failed']}\n")
            self.stdout.write(f"\nThe time to retry all transactions was {finish}\n")
        except Exception as e:
            raise CommandError(f"\n-----AN ERROR HAS BEEN RAISED WHILE RETRYING SAGEX3 FAILED TRANSACTIONS: {e}")
