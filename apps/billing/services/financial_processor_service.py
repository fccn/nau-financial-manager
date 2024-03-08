from apps.billing.models import Transaction


class TransactionProcessorInterface:
    """
    This class represents an interface to be implemented as a contract.

    Each new transaction processor needs to implements its logic by signing to this class.
    """

    transaction: Transaction = None

    def __init__(self, transaction: Transaction) -> None:
        self.transaction = transaction

    def send_transaction_to_processor(self) -> dict:
        """
        This method sends the transaction to the processor.
        """
        raise Exception("This method needs to be implemented")

    @property
    def data(self):
        """
        Generates the request data from the transaction, as expected for the service.
        """
        raise Exception("This method needs to be implemented")
