from apps.billing.models import Transaction
from apps.billing.services.financial_processor_service import ProcessorInstantiator, TransactionProcessorInterface
from apps.billing.services.processor_service import SageX3Processor


class TransactionService:
    """
    This class is the TransactionService, from here will be triggered the steps to check and send
    a transaction to the transaction processor.
    """

    def __init__(self) -> None:
        self.__processor: TransactionProcessorInterface = ProcessorInstantiator(processor=SageX3Processor)

    def __send_transaction(self, trasaction: Transaction):
        self.__processor.send_transaction_to_processor(data={})

    def __check_transaction(self):
        self.__processor.check_transaction_in_processor()

    def run_transaction_steps(self):
        try:
            transaction_already_registered: bool = self.__check_transaction()
            if not transaction_already_registered:
                document_id = self.__send_transaction()

                return document_id
        except Exception as e:
            raise e
