from decimal import Decimal

import factory
import factory.fuzzy
from django.utils import timezone

from apps.billing.models import Transaction, TransactionItem
from apps.util.constants import PAYMENT_TYPE, TRANSACTION_TYPE


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    transaction_id = factory.Faker(
        "pystr_format",
        string_format="NAU-######{random_int}",
    )
    client_name = factory.Faker("name")
    email = factory.Faker("email")
    address_line_1 = factory.Faker("address")
    address_line_2 = factory.Faker("address")
    country_code = factory.Faker("country_code")
    vat_identification_country = factory.Faker("country_code")
    vat_identification_number = factory.Faker("ssn")
    total_amount_exclude_vat = factory.Faker("pydecimal", min_value=1, max_value=100, left_digits=5, right_digits=2)
    payment_type = factory.fuzzy.FuzzyChoice(PAYMENT_TYPE)
    transaction_type = factory.fuzzy.FuzzyChoice(TRANSACTION_TYPE)
    transaction_date = factory.Faker(
        "date_time_between", start_date="-1d", end_date="-5d", tzinfo=timezone.get_current_timezone()
    )
    document_id = factory.Faker("pystr_format", string_format="DCI-######{random_int}")

    # Assuming 20% VAT
    @factory.lazy_attribute
    def total_amount_include_vat(self):
        return self.total_amount_exclude_vat * Decimal("1.20")


class TransactionItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TransactionItem

    transaction = factory.SubFactory(TransactionFactory)
    description = factory.Faker("sentence")
    quantity = factory.Faker("pyint", min_value=1, max_value=10)
    vat_tax = factory.Faker("pydecimal", min_value=1, max_value=100, left_digits=3, right_digits=2)
    amount_exclude_vat = factory.Faker("pydecimal", min_value=1, max_value=100, left_digits=5, right_digits=2)
    organization = factory.Faker("ean13")
    product_code = factory.Faker("ean13")
    product_id = factory.Faker("uuid4")

    # Assuming 20% VAT
    @factory.lazy_attribute
    def amount_include_vat(self):
        return self.amount_exclude_vat * Decimal("1.20")
