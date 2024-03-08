import logging
import traceback

import xmltodict

from apps.billing.models import SageX3TransactionInformation, Transaction
from apps.billing.services.financial_processor_service import TransactionProcessorInterface
from apps.billing.services.processor_service import SageX3Processor

log = logging.getLogger(__name__)


class TransactionService:
    """
    This class is the TransactionService, from here will be triggered the steps to check and send
    a transaction to the transaction processor.
    """

    def __init__(
        self,
        transaction: Transaction,
    ) -> None:
        """
        Initialize a TransactionService and save the necessary information marking
        that there is a pending transaction to be sent.
        """
        self.transaction = transaction
        self.__processor: TransactionProcessorInterface = SageX3Processor(transaction)
        SageX3TransactionInformation.objects.get_or_create(transaction=transaction)

    def __save_transaction_xml(self, transaction: Transaction, informations: dict) -> None:
        """
        Saves the XML content of a transaction to the database.

        This function attempts to get or create a SageX3TransactionInformation object
        with the given transaction. If the SageX3TransactionInformation object doesn't exist,
        it creates one with the provided XML content. If an exception occurs during
        this process, it prints the exception message.
        """
        try:
            obj, created = SageX3TransactionInformation.objects.get_or_create(
                transaction=transaction, defaults={**informations}
            )
            if not created:
                obj.retries += 1
                obj.status = informations["status"]
                obj.save()

        except Exception as e:
            log.exception("Some error has occurred saving the transaction xml")
            raise e

    @staticmethod
    def extract_document_id_from_response(response) -> str:
        """
        Extracts the document_id from the Sage X3 response or None if didn't find it.
        """
        response_as_json = dict(xmltodict.parse(response))
        response_as_json = response_as_json["soapenv:Envelope"]["soapenv:Body"]

        if "multiRef" in list(dict(response_as_json).keys()):
            message = "Nº Fatura NAU já registada no documento: "
            if message in response_as_json["multiRef"]["message"]:
                document_id = response_as_json["multiRef"]["message"].replace(message, "")

                return document_id

        result = xmltodict.parse(response_as_json["wss:saveResponse"]["saveReturn"]["resultXml"]["#text"])
        document_id = None
        for r in result["RESULT"]["GRP"]:
            for field in r["FLD"]:
                if field["@NAME"] == "NUM":
                    document_id = field["#text"]
                    break

            if document_id:
                break

        return document_id

    def run_steps_to_send_transaction(self):
        data = None
        try:
            response = self.__processor.send_transaction_to_processor()
            document_id = self.__class__.extract_document_id_from_response(response)
            data = self.__processor.data
            self.__save_transaction_xml(
                informations={"input_xml": data, "error_messages": "", "status": SageX3TransactionInformation.SUCCESS},
                transaction=self.transaction,
            )
            # save the document_id so we know what have been created on SageX3
            self.transaction.document_id = document_id
            self.transaction.save()
        except Exception as e:
            # log the exception and eat it.
            log.exception(f"An exception has been raised when sending data to processor, exception message={e}")
            exception_stack_trace = traceback.format_exc()
            self.__save_transaction_xml(
                informations={
                    "input_xml": data,
                    "error_messages": exception_stack_trace,
                    "status": SageX3TransactionInformation.FAILED,
                },
                transaction=self.transaction,
            )
