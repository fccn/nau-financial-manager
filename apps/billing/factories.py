import random
import string
from decimal import Decimal

import factory
import factory.fuzzy
from django.conf import settings
from django.utils import timezone

from apps.billing.mocks import xml_duplicate_error_response_mock
from apps.billing.models import SageX3TransactionInformation, Transaction, TransactionItem
from apps.util.constants import PAYMENT_TYPE, TRANSACTION_TYPE


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    transaction_id = factory.Faker(
        "pystr_format",
        string_format="NAU-######{{random_int}}",
    )
    client_name = factory.Faker("name")
    email = factory.Faker("email")
    address_line_1 = factory.Faker("address")
    address_line_2 = factory.Faker("address")
    city = "City"
    postal_code = factory.Faker(
        "pystr_format",
        string_format="%%%%-%%%",
    )
    state = "State"
    country_code = factory.Faker("country_code")
    vat_identification_country = factory.Faker("country_code")
    vat_identification_number = factory.Faker("ssn")
    total_amount_exclude_vat = factory.Faker("pydecimal", min_value=1, max_value=100, left_digits=5, right_digits=2)
    payment_type = factory.fuzzy.FuzzyChoice(PAYMENT_TYPE)
    transaction_type = factory.Faker("random_element", elements=[t[0] for t in TRANSACTION_TYPE])
    transaction_date = factory.Faker(
        "date_time_between", start_date="-5d", end_date="-1d", tzinfo=timezone.get_current_timezone()
    )
    document_id = factory.Faker("pystr_format", string_format="DCI-######{{random_int}}")

    @factory.lazy_attribute
    def total_amount_include_vat(self):
        return round(self.total_amount_exclude_vat * Decimal("1.23"), 2)


class TransactionItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TransactionItem

    transaction = factory.SubFactory(TransactionFactory)
    description = factory.Faker("sentence")
    quantity = factory.Faker("pyint", min_value=1, max_value=10)
    vat_tax = factory.Faker("pydecimal", min_value=1, max_value=100, left_digits=3, right_digits=2)
    organization_code = factory.Sequence(lambda n: f"Org {n}")
    product_code = "".join([random.choice(string.ascii_uppercase) for _ in range(5)])
    discount = factory.Faker("pydecimal", min_value=0, max_value=1, left_digits=1, right_digits=2)

    @factory.lazy_attribute
    def product_id(self):
        return f"course-v1:{self.organization_code}+{self.product_code}+2023_T3"

    @factory.lazy_attribute
    def unit_price_excl_vat(self):
        return round((self.transaction.total_amount_exclude_vat / self.quantity), 2)

    @factory.lazy_attribute
    def unit_price_incl_vat(self):
        return round(((self.transaction.total_amount_include_vat * Decimal("1.20")) / self.quantity), 2)


class SageX3TransactionInformationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SageX3TransactionInformation

    transaction = factory.SubFactory(TransactionFactory)
    status = factory.Faker("random_element", elements=SageX3TransactionInformation.STATE_CHOICES)
    last_status_date = factory.Faker(
        "date_time_between", start_date="-5d", end_date="-1d", tzinfo=timezone.get_current_timezone()
    )
    retries = factory.Faker("pyint", min_value=0, max_value=10)
    series = getattr(settings, "DEFAULT_SERIES")

    @factory.lazy_attribute
    def input_xml(self):
        return "<xml></xml>"

    @factory.lazy_attribute
    def output_xml(self):
        return xml_duplicate_error_response_mock()
