import json

import requests
from django.conf import settings


class ReceiptDocumentHost:
    def __init__(self) -> None:
        self.__receipt_host_url = getattr(settings, "RECEIPT_HOST_URL")
        self.__receipt_bearer_token = getattr(settings, "RECEIPT_BEARER_TOKEN")
        self.__receipt_entity_public_key = getattr(settings, "RECEIPT_ENTITY_PUBLIC_KEY")

    def __check_status_code(self, response: requests.Response):
        try:
            assert response.status_code not in [401, 404, 500]
        except Exception:
            raise requests.exceptions.RequestException(response=response)

    def get_document(self, document_id: str):
        """
        This method gets the file url, it calls the receipt host giving the required parameters.

        The `document_id` is a transaction parameter, it is the returned id from the transaction processor.
        The `__receipt_bearer_token` is setted in the environment.
        """
        response = requests.get(
            url=f"{self.__receipt_host_url}/{document_id}",
            headers={
                "entity": self.__receipt_entity_public_key,
                "Authorization": f"Bearer {self.__receipt_bearer_token}",
            },
        )
        self.__check_status_code(response=response)
        response = response.content
        response = json.JSONDecoder().decode(response)
        document_informations = [
            attachment for attachment in response["response"]["data"]["attachments"] if attachment["type"] == "pdf"
        ][0]

        return document_informations["file"]
