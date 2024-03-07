from celery import shared_task
from django.db import transaction as db_transaction

from apps.billing.models import Transaction
from apps.billing.services.transaction_service import TransactionService


@shared_task(name="apps.billing.tasks.create_and_async_send_transactions_to_processor_task")
def create_and_async_send_transactions_to_processor_task(transaction: Transaction):
    # create the Transaction Service that will initialize the internal objects
    # and mark it to pending to be sent.
    with db_transaction.atomic():
        TransactionService(transaction=transaction)

    transaction.refresh_from_db()

    # send
    TransactionService(transaction=transaction).run_steps_to_send_transaction()
