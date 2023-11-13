from apps.billing.services.financial_processor_service import TransactionProcessor


class SageX3Processor(TransactionProcessor):
    def send_transaction_to_processor(self, data):
        pass

    def check_transaction_in_processor(self):
        pass
