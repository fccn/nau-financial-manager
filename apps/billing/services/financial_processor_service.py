from apps.billing.models import Transaction


class TransactionProcessorInterface:
    """
    This class represents an interface to be implemented as a contract.

    Each new transcation processor needs to implements its logic by signing to this class.
    """

    transaction: Transaction = None

    def send_transaction_to_processor(self) -> dict:
        raise Exception("This method needs to be implemented")

    @property
    def data(self):
        raise Exception("This method needs to be implemented")
