from typing import TypeVar


class TransactionProcessor:
    def send_transaction_to_processor(self, data):
        pass

    def check_transaction_in_processor(self):
        pass


T = TypeVar("T", TransactionProcessor)


class FinancialProcessorService(T):
    pass
