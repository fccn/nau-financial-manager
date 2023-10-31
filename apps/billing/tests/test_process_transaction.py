import factory
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.billing.factories import TransactionFactory, TransactionItemFactory
from apps.billing.models import Transaction
from apps.billing.serializers import TransactionItemSerializer, TransactionSerializer


class ProcessTransactionTest(TestCase):
    """
    A test case for the ProcessTransaction view.
    """

    def setUp(self):
        """
        Set up the test case by creating a client, endpoint, transaction, transaction item, and payload.
        Also create a new user and generate a token for that user.
        """
        self.client = APIClient()
        self.endpoint = "/api/billing/transaction-complete/"

        self.transaction = factory.build(dict, FACTORY_CLASS=TransactionFactory)
        self.transaction_item = factory.build(dict, FACTORY_CLASS=TransactionItemFactory, transaction=None)
        self.transaction["item"] = self.transaction_item
        self.payload = self.transaction

        # Create a new user and generate a token for that user
        self.user = get_user_model().objects.create_user(username="testuser", password="testpass")
        self.token = Token.objects.create(user=self.user)

    def test_create_transaction(self):
        """
        Test that a transaction can be created with a valid token.
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.post(self.endpoint, self.payload, format="json")
        self.assertEqual(response.status_code, 201)

        transaction = Transaction.objects.get(transaction_id=self.payload["transaction_id"])
        transaction_data = TransactionSerializer(transaction).data
        transaction_data["item"] = TransactionItemSerializer(transaction.transaction_items.all()[0]).data

        for key, value in response.data["data"].items():
            if key == "item":
                for item_key, item_value in response.data["data"]["item"].items():
                    self.assertEqual(item_value, transaction_data["item"][item_key])
            self.assertEqual(value, transaction_data[key])

    def test_create_transaction_without_token(self):
        """
        Test that a transaction cannot be created without a valid token.
        """
        response = self.client.post(self.endpoint, self.payload, format="json")
        self.assertEqual(response.status_code, 401)

    def test_create_transaction_with_duplicate_transaction_id(self):
        """
        Test that a transaction cannot be created with a duplicate transaction ID.
        """
        # Create a new transaction with the same transaction ID as the payload
        TransactionFactory.create(transaction_id=self.payload["transaction_id"])

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.post(self.endpoint, self.payload, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_transaction_with_invalid_fields(self):
        """
        Test that a transaction cannot be created if fields are invalid.
        """
        # Set the 'amount' field to an invalid value
        self.payload["amount"] = "invalid_amount"

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.post(self.endpoint, self.payload, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_transaction_with_missing_fields(self):
        """
        Test that a transaction cannot be created if required fields are missing.
        """
        # Remove the required 'transaction_id' field from the payload
        del self.payload["transaction_id"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.post(self.endpoint, self.payload, format="json")
        self.assertEqual(response.status_code, 400)

    def test_create_transaction_with_invalid_token(self):
        """
        Test that a transaction cannot be created with an invalid token.
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + "invalid_token")

        response = self.client.post(self.endpoint, self.payload, format="json")
        self.assertEqual(response.status_code, 401)

    def test_create_transaction_with_missing_item_field(self):
        """
        Test that a transaction cannot be created if the 'item' field is missing.
        """
        # Remove the required 'item' field from the payload
        del self.payload["item"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.post(self.endpoint, self.payload, format="json")
        self.assertEqual(response.status_code, 400)
