from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from apps.billing.models import Transaction
from apps.billing.serializers import ProcessTransactionSerializer


class ProcessTransactionTest(TestCase):
    def setUp(self):
        self.payload = {
            "transaction_id": "a9k05000-227f-4500-b71f-9f00fba1cf5f",
            "client_name": "Cliente name",
            "email": "cliente@email.com",
            "address_line_1": "Av. Liberdade",
            "address_line_2": "",
            "city": "Lisboa",
            "postal_code": "1250-142",
            "state": "",
            "country_code": "PT",
            "vat_identification_number": "PT220234835",
            "vat_identification_country": "PT",
            "total_amount_exclude_vat": 114.73,
            "total_amount_include_vat": 149.00,
            "currency": "EUR",
            "item": {
                "description": "The product/line text with a description of what have been bought. The field need to be a string.",
                "quantity": 1,
                "vat_tax": 114.73,
                "amount_exclude_vat": 114.73,
                "amount_include_vat": 149.00,
                "organization_code": "UPorto",
                "product_id": "course-v1:UPorto+CBNEEF+2023_T3",
                "product_code": "CBNEEF",
            },
        }
        self.client = APIClient()
        self.endpoint = "/api/billing/transaction-complete/"

        # Create a new user and generate a token for that user
        self.user = get_user_model().objects.create_user(username="testuser", password="testpass")
        self.token = Token.objects.create(user=self.user)

    def test_create_transaction(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.post(self.endpoint, self.payload, format="json")
        self.assertEqual(response.status_code, 201)

        transaction = Transaction.objects.get(transaction_id=self.payload["transaction_id"])
        serializer = ProcessTransactionSerializer(transaction)

        self.assertEqual(response.data, serializer.data)

    def test_create_transaction_without_token(self):
        response = self.client.post(self.endpoint, self.payload, format="json")
        self.assertEqual(response.status_code, 401)
