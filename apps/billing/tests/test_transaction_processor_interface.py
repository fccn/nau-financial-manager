from django.test.testcases import TestCase

from apps.billing.services.financial_processor_service import TransactionProcessorInterface

class TransactionServiceTestCase(TestCase):
    """
    Tests the `TransactionService`
    """

    def test_financial_processor_service_interface(self):
        """
        This test ensures that if not implemented, the method from the interface
        will raise an exception.
        """
        with self.assertRaisesMessage(
            expected_exception=Exception,
            expected_message="This method needs to be implemented",
        ):
            TransactionProcessorInterface(None).send_transaction_to_processor()
