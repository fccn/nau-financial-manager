import decimal
import json
import logging
from copy import deepcopy
from unittest import mock

import factory
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.billing.factories import TransactionFactory, TransactionItemFactory
from apps.billing.models import SageX3TransactionInformation, Transaction
from apps.billing.serializers import TransactionItemSerializer, TransactionSerializer

from .test_transaction_service import processor_success_response

log = logging.getLogger(__name__)


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

    @mock.patch("requests.post", side_effect=processor_success_response)
    def test_create_transaction(self, mock):
        """
        Test that a transaction can be created with a valid token.
        """
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        log.info(self.payload)
        response = self.client.post(self.endpoint, self.payload, format="json")
        log.info(response.content)
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

        self.assertTrue(SageX3TransactionInformation.objects.filter(transaction=transaction).exists())

    @mock.patch("requests.post", side_effect=processor_success_response)
    def test_doest_not_send_transaction_with_zero_as_total_amount(self, mock):
        """
        Test that a transaction will not be sent to the processor if the total amound sold is zero.
        """
        payload = deepcopy(self.payload)
        payload["total_amount_exclude_vat"] = 0
        payload["total_amount_include_vat"] = 0
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        log.info(payload)
        response = self.client.post(self.endpoint, payload, format="json")
        log.info(response.content)
        self.assertEqual(response.status_code, 201)

        transaction = Transaction.objects.get(transaction_id=payload["transaction_id"])
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

        self.assertFalse(SageX3TransactionInformation.objects.filter(transaction=transaction).exists())

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

    @mock.patch("requests.post", side_effect=processor_success_response)
    def test_valid_transaction_item_discount(self, mock):
        """
        This test ensures that is possible to process a transaction with valid discount value in items
        """

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.post(self.endpoint, self.payload, format="json")

        for item in self.payload["items"]:
            self.assertTrue(decimal.Decimal(item["discount_excl_tax"]) == 0.0)
            self.assertTrue(decimal.Decimal(item["discount_incl_tax"]) == 0.0)

        self.assertEqual(response.status_code, 201)

    # def test_invalid_transaction_item_discount_greater_than_1(self):
    #     """
    #     This test ensures that is not possible to process a transaction with invalid discount value in items
    #     """

    #     self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
    #     invalid_payload = deepcopy(self.payload)
    #     invalid_payload["items"][0]["total_discount_incl_tax"] = 1.1
    #     response = self.client.post(self.endpoint, invalid_payload, format="json")

    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(str(response.data["total_discount_incl_tax"][0]), "Ensure this value is less than or equal to 1.")

    # def test_invalid_transaction_item_discount_smaller_than_0(self):
    #     """
    #     This test ensures that is not possible to process a transaction with invalid discount value in items
    #     """

    #     self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
    #     invalid_payload = deepcopy(self.payload)
    #     invalid_payload["items"][0]["discount"] = -1
    #     response = self.client.post(self.endpoint, invalid_payload, format="json")

    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(str(response.data["discount"][0]), "Ensure this value is greater than or equal to 0.")

    # @mock.patch("requests.post", side_effect=processor_success_response)
    # def test_invalid_transaction_item_discount_none(self, mock):
    #     """
    #     This test ensures that is not possible to process a transaction without a discount value in items
    #     """

    #     self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
    #     invalid_payload = deepcopy(self.payload)
    #     invalid_payload["items"][0].pop("discount", None)
    #     response = self.client.post(self.endpoint, invalid_payload, format="json")

    #     self.assertEqual(response.status_code, 201)
