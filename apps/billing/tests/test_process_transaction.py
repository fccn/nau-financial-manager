import json

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

        transaction = TransactionFactory.build()
        item = TransactionItemFactory.build(transaction=transaction)

        self.transaction = factory.build(dict, **TransactionSerializer(transaction).data)
        self.transaction_item = factory.build(dict, **TransactionItemSerializer(item).data)
        self.transaction["items"] = [self.transaction_item]

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
        transaction_data["items"] = [
            TransactionItemSerializer(item).data for item in transaction.transaction_items.all()
        ]

        for key, value in dict(response.data["data"]).items():
            if key == "items":
                for item in value:
                    same_item = [i for i in transaction_data["items"] if i == item][0]
                    [self.assertEqual(v, same_item[k]) for k, v in dict(item).items()]

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
        response_data_message = json.loads(response.content)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_data_message["transaction_id"][0], "transaction with this transaction id already exists."
        )

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
        Test that a transaction cannot be created if the 'items' field is missing.
        """
        # Remove the required 'items' field from the payload
        del self.payload["items"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.post(self.endpoint, self.payload, format="json")
        self.assertEqual(response.status_code, 400)
