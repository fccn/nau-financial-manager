import json
from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase
from requests import Response
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.billing.factories import TransactionFactory
from apps.billing.mocks import ILINK_RESPONSE_MOCK
from apps.billing.models import Transaction
from apps.billing.services.receipt_host_service import ReceiptDocumentHost


class ReceiptDocumentHostForTest(ReceiptDocumentHost):
    def __init__(self) -> None:
        self.__receipt_host_url = "https://receipt-fake.com/"
        self.__receipt_host_auth = "test_auth"
        self.__receipt_host_password = "pwd_test"
        self.__receipt_entity_public_key = "receipt_entity_public_key"


class MockResponse(Response):
    def __init__(self, data, status_code):
        self.data = data
        self.status_code = status_code

    @property
    def content(self):
        return json.JSONEncoder().encode(o=self.data)


def mocked_get(*args, **kwargs):
    return MockResponse(data=ILINK_RESPONSE_MOCK, status_code=200)


class ReceiptDocumentHostTest(TestCase):
    def setUp(self) -> None:
        """
        This method starts the `ReceiptDocumentHostTest` compoment,
        setting the required parameters to excute the tests.
        """

        user = get_user_model().objects.create(username="user_test", password="pwd_test")
        self.token = Token.objects.create(user=user)
        self.api_client = APIClient()
        self.receipt_document_host = ReceiptDocumentHostForTest()
        self.transaction: Transaction = TransactionFactory.create()

    @mock.patch("requests.get", mocked_get)
    def test_get_document_success(self):
        """
        This test ensures to success getting a file link providing the
        transaction_id though the url.
        """

        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        link = ILINK_RESPONSE_MOCK["response"]["data"]["attachments"][0]["file"]
        response = self.api_client.get(f"/api/billing/receipt-link/{self.transaction.transaction_id}/")
        obtained_link = response.data["response"]

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data))
        self.assertTrue(isinstance(response.data, dict))
        self.assertTrue(len(response.data.values()))
        self.assertTrue(isinstance(obtained_link, str))
        self.assertTrue(obtained_link is not None and obtained_link.lstrip() != "")
        self.assertEqual(link, obtained_link)

    def test_get_document_transaction_not_found(self):
        """
        This test ensures the transaction not found error getting a file link providing wrong
        transaction id parameter.
        """

        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        response = self.api_client.get("/api/billing/receipt-link/wrong-transaction-id/")
        data = response.data["response"]

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, "Trasaction not found")

    def test_get_document_authentication_not_provided(self):
        """
        This test ensures the authentication not provided error getting a file link
        without credentials.
        """

        self.api_client.credentials()

        response = self.api_client.get("/api/billing/receipt-link/wrong-transaction-id/")
        content = response.content.decode()
        message = json.JSONDecoder().decode(s=content)
        message = message["error"]["message"]["detail"]

        self.assertEqual(response.status_code, 401)
        self.assertEqual(message, "Authentication credentials were not provided.")

    def test_get_document_invalid_token(self):
        """
        This test ensures the invalid token error getting a file link
        providing a invalid token.
        """

        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key[:-3]}abc")

        response = self.api_client.get("/api/billing/receipt-link/wrong-transaction-id/")
        content = response.content.decode()
        message = json.JSONDecoder().decode(s=content)
        message = message["error"]["message"]["detail"]

        self.assertEqual(response.status_code, 401)
        self.assertEqual(message, "Invalid token.")

    def test_get_document_endpoint_not_found(self):
        """
        This test ensures the not found error getting a file link calling a wrong url.
        """

        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key[:-3]}abc")

        response = self.api_client.get("/api/billing/receipt-link/")

        self.assertEqual(response.status_code, 404)
