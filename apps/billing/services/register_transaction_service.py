from apps.billing.services.financial_processor_service import FinancialProcessorService
from apps.billing.services.processor_service import SageX3Processor


class RegisterTransactionService:
    def send_transaction(self):
        FinancialProcessorService[SageX3Processor]().send_transaction_to_processor()

    def check_transaction(self):
        FinancialProcessorService[SageX3Processor]().check_transaction_in_processor()
