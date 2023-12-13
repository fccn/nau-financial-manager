from celery import shared_task

from apps.billing.models import Transaction
from apps.billing.services.transaction_service import TransactionService


@shared_task(name="apps.billing.tasks.send_transactions_to_processor_task")
def send_transactions_to_processor_task(transaction: Transaction):
    try:
        document_id: str = TransactionService(transaction=transaction).run_steps_to_send_transaction()
        transaction.document_id = document_id
        transaction.save()
    except Exception as e:
        raise e
