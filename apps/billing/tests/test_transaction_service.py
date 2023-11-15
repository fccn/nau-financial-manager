from django.test.testcases import TestCase

from apps.billing.services.financial_processor_service import ProcessorInstantiator, TransactionProcessorInterface
from apps.billing.services.processor_service import SageX3Processor
from apps.billing.services.transaction_service import TransactionService


class TransactionServiceTestCase(TestCase):
    def setUp(self) -> None:
        self.financial_processor_interface = TransactionProcessorInterface()
        self.transaction_service = TransactionService()
        self._transaction_processor = SageX3Processor()
        return super().setUp()

    def test_financial_processor_service(self):
        with self.assertRaisesMessage(
            expected_exception=Exception,
            expected_message="This method needs to be implemented",
        ):
            self.financial_processor_interface.check_transaction_in_processor()
            self.financial_processor_interface.send_transaction_to_processor(transaction_data={})

    def test_processor_instance(self):
        processor = ProcessorInstantiator(processor=SageX3Processor)

        self.assertEqual(type(processor), SageX3Processor)
        self.assertTrue(isinstance(processor, TransactionProcessorInterface))

    def test_processor_service(self):
        transaction_already_registered = self._transaction_processor.check_transaction_in_processor()
        document_id = self._transaction_processor.send_transaction_to_processor(transaction_data={})

        self.assertEqual(type(transaction_already_registered), bool)
        self.assertEqual(type(document_id), str)
