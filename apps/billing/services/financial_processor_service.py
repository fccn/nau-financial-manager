from apps.billing.models import Transaction


class TransactionProcessorInterface:
    """
    This class represents an interface to be implemented as a contract.

    Each new transcation processor needs to implements its logic by signing to this class.
    """

    def send_transaction_to_processor(self, transaction: Transaction) -> str:
        raise Exception("This method needs to be implemented")

    def check_transaction_in_processor(self, transaction: Transaction) -> bool:
        raise Exception("This method needs to be implemented")


class ProcessorInstantiator:
    """
    This class is a instantiator module for the `TransactionProcessorInterface` type.

    The business logic implemented here, deals with invert the dependency for the type `TransactionProcessorInterface`,
    then a new transaction processor can replace an older without many problems.
    """

    def __new__(cls, processor: TransactionProcessorInterface) -> TransactionProcessorInterface:
        if not issubclass(processor, TransactionProcessorInterface):
            raise Exception("The given processor is not from the type of TransactionProcessorInterface")

        instance = processor()

        if not isinstance(instance, TransactionProcessorInterface):
            raise Exception("The generated processor instance is not from the type of TransactionProcessorInterface")

        return instance
