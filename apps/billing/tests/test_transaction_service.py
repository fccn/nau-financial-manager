from django.conf import settings
from django.test.testcases import TestCase

from apps.billing.factories import TransactionFactory, TransactionItemFactory
from apps.billing.mock_server import run_mock_server
from apps.billing.services.financial_processor_service import ProcessorInstantiator, TransactionProcessorInterface
from apps.billing.services.processor_service import SageX3Processor
from apps.billing.services.transaction_service import TransactionService


class TransactionServiceTestCase(TestCase):
    def setUp(self) -> None:
        self.financial_processor_interface = TransactionProcessorInterface()
        self.transaction_service = TransactionService()
        self._transaction_processor = SageX3Processor()
        self.transaction = TransactionFactory.create()
        self.transaction_item = TransactionItemFactory.create(transaction=self.transaction)
        self.processor_url = getattr(settings, "TRANSACTION_PROCESSOR_URL")

        return super().setUp()

    def test_financial_processor_service(self):
        with self.assertRaisesMessage(
            expected_exception=Exception,
            expected_message="This method needs to be implemented",
        ):
            self.financial_processor_interface.check_transaction_in_processor(transaction=self.transaction)
            self.financial_processor_interface.send_transaction_to_processor(transaction=self.transaction)

    def test_processor_instance(self):
        processor = ProcessorInstantiator(processor=SageX3Processor)

        self.assertEqual(type(processor), type(self._transaction_processor))
        self.assertEqual(type(processor), SageX3Processor)
        self.assertTrue(isinstance(processor, TransactionProcessorInterface))

    def test_transaction_processor(self):
        self.mock_server, self.thread = run_mock_server()
        processor: SageX3Processor = ProcessorInstantiator(processor=SageX3Processor)
        response = processor.send_transaction_to_processor(transaction=self.transaction)

        self.assertTrue(response)
        self.assertEqual(type(response), dict)

    def tearDown(self) -> None:
        if hasattr(self, "mock_server"):
            setattr(settings, "TRANSACTION_PROCESSOR_URL", self.processor_url)
            self.mock_server.shutdown()
            self.thread.join()

        return super().tearDown()
