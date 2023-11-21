import xmltodict

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

    def __check_transaction_state(self, document_id):
        pass

    def __send_transaction_to_processor(self, transaction: Transaction) -> str:
        """
        This method receives a Transaction to send to the processor and deals with the request result.

        From the result is extracted the document id, which is provided to invocate the `__check_transaction_state`
        method, that checks and updates the transaction status.
        """

        try:
            response_from_service = self.__processor.send_transaction_to_processor(transaction=transaction)
            response_from_service = response_from_service["soapenv:Envelope"]["soapenv:Body"]

            if "multiRef" in list(dict(response_from_service).keys()):
                message = "Nº Fatura NAU já registada no documento: "
                if message in response_from_service["multiRef"]["message"]:
                    document_id = response_from_service["multiRef"]["message"].replace(message, "")
                    self.__check_transaction_state(document_id=document_id)

                    return document_id

            result = xmltodict.parse(response_from_service["wss:saveResponse"]["saveReturn"]["resultXml"]["#text"])
            document_id = ""
            for r in result["RESULT"]["GRP"]:
                for field in r["FLD"]:
                    if field["@NAME"] == "NUM":
                        document_id = field["#text"]
                        break

                if document_id:
                    break

            return document_id
        except Exception as e:
            raise e

    def run_steps_to_send_transaction(self, transaction: Transaction) -> None:
        try:
            document_id = self.__send_transaction_to_processor(transaction=transaction)
            self.__check_transaction_state(document_id=document_id)
        except Exception as e:
            raise e
