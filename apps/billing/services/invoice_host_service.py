import json

import requests
from django.conf import settings


class InvoiceDocumentHost:
    def __init__(self) -> None:
        self.__invoice_host_url = getattr(settings, "INVOICE_HOST_URL")
        self.__invoice_host_auth = getattr(settings, "INVOICE_HOST_AUTH")
        self.__invoice_host_password = getattr(settings, "INVOICE_HOST_PASSWORD")

    def get_document(self, document_id: str):
        """
        This method gets the file url, it calls the invoice host giving the required parameters.

        document_id comes from the transaction. It is the returned id from the transaction processor.
        __invoice_host_auth and  __invoice_host_password is setted in the environment.
        """

        try:
            response = requests.get(
                url=f"{self.__invoice_host_url}/{document_id}",
                auth=(
                    self.__invoice_host_auth,
                    self.__invoice_host_password,
                ),
            ).content
            response = json.JSONDecoder().decode(response)
            document_informations = [
                attachment for attachment in response["response"]["data"]["attachments"] if attachment["type"] == "pdf"
            ][0]
            return document_informations["file"]
        except Exception as e:
            raise e
