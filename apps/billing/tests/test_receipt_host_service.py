import json
from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.billing.factories import TransactionFactory
from apps.billing.mocks import ILINK_RESPONSE_MOCK, UNAUTHORIZED_ILINK_RESPONSE, MockResponse
from apps.billing.models import Transaction


@override_settings(
    RECEIPT_HOST_URL="https://receipt-fake.com/",
    RECEIPT_BEARER_TOKEN="receipt_entity_public_key",
    RECEIPT_ENTITY_PUBLIC_KEY="Bearer token",
)
class ReceiptDocumentHostTest(TestCase):
    def setUp(self) -> None:
        """
        This method starts the `ReceiptDocumentHostTest` compoment,
        setting the required parameters to excute the tests.
        """

        user = get_user_model().objects.create(username="user_test", password="pwd_test")
        self.token = Token.objects.create(user=user)
        self.api_client = APIClient()
        self.transaction: Transaction = TransactionFactory.create()

    @mock.patch("requests.get", return_value=MockResponse(data=ILINK_RESPONSE_MOCK, status_code=200))
    def test_get_document_success(self, mocked_post):
        """
        This test ensures to success getting a file link providing the
        transaction_id though the url.
        """

        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        response = self.api_client.get(f"/api/billing/receipt-link/{self.transaction.transaction_id}/")
        obtained_link = response.data["response"]

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(obtained_link, str))
        self.assertTrue(obtained_link is not None and obtained_link.lstrip() != "")
        self.assertEqual(ILINK_RESPONSE_MOCK["response"]["data"][0]["attachments"][0]["file"], obtained_link)

        mocked_post.assert_called_once()
        _, _, kwargs = mocked_post.mock_calls[0]
        self.assertEqual("https://receipt-fake.com/", kwargs.get("url"))
        self.assertDictEqual(
            {"document_type": "issued", "document_number": self.transaction.document_id}, kwargs.get("params")
        )

    def test_get_document_transaction_not_found(self):
        """
        This test ensures the transaction not found error getting a file link providing wrong
        transaction id parameter.
        """

        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        response = self.api_client.get("/api/billing/receipt-link/wrong-transaction-id/")
        data = response.data["response"]

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, "Transaction not found")

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

        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

        response = self.api_client.get("/api/billing/receipt-link/")

        self.assertEqual(response.status_code, 404)

    @mock.patch("requests.get", lambda *args, **kwargs: MockResponse("File not found", status_code=404))
    def test_get_document_file_not_found(self):
        """
        This test ensures that the file not found exception is correctly handled.
        """

        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

        response = self.api_client.get(f"/api/billing/receipt-link/{self.transaction.transaction_id}/")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["response"], "File not found")

    @mock.patch("requests.get", return_value=MockResponse(UNAUTHORIZED_ILINK_RESPONSE, status_code=500))
    def test_get_document_unauthorized(self, mocked_post):
        """
        This test ensures that the unauthorized exception is correctly handled.
        """

        self.api_client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

        response = self.api_client.get(f"/api/billing/receipt-link/{self.transaction.transaction_id}/")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.data["response"], "Occurred an error getting the document")
