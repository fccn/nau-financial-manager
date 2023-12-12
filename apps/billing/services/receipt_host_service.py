import json

import requests
from django.conf import settings


class ReceiptDocumentHost:
    def __init__(self) -> None:
        self.__receipt_host_url = getattr(settings, "RECEIPT_HOST_URL")
        self.__receipt_host_auth = getattr(settings, "RECEIPT_HOST_AUTH")
        self.__receipt_host_password = getattr(settings, "RECEIPT_HOST_PASSWORD")

    def get_document(self, document_id: str):
        """
        This method gets the file url, it calls the receipt host giving the required parameters.

        document_id comes from the transaction. It is the returned id from the transaction processor.
        __receipt_host_auth and  __receipt_host_password is setted in the environment.
        """

        try:
            response = requests.get(
                url=f"{self.__receipt_host_url}/{document_id}",
                auth=(
                    self.__receipt_host_auth,
                    self.__receipt_host_password,
                ),
            ).content
            response = json.JSONDecoder().decode(response)
            document_informations = [
                attachment for attachment in response["response"]["data"]["attachments"] if attachment["type"] == "pdf"
            ][0]
            return document_informations["file"]
        except Exception as e:
            raise e
