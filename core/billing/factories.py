from decimal import Decimal

import factory

from core.billing.models import Receipt, ReceiptLine


class ReceiptFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Receipt

    name = factory.Faker("name")
    email = factory.Faker("email")
    address = factory.Faker("address")
    vat_identification_country = factory.Faker("country_code")
    vat_identification_number = factory.Faker("ssn")
    total_amount_exclude_vat = factory.Faker("pydecimal", left_digits=5, right_digits=2)
    total_amount_include_vat = factory.LazyAttribute(
        lambda o: o.total_amount_exclude_vat * Decimal("1.20")
    )  # Assuming 20% VAT
    receipt_link = factory.Faker("url")
    receipt_document_id = factory.Faker("uuid4")


class ReceiptLineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReceiptLine

    receipt = factory.SubFactory(ReceiptFactory)
    description = factory.Faker("sentence")
    quantity = factory.Faker("pyint", min_value=1, max_value=10)
    vat_tax = factory.Faker("pydecimal", left_digits=3, right_digits=2)
    amount_exclude_vat = factory.Faker("pydecimal", left_digits=5, right_digits=2)
    amount_include_vat = factory.LazyAttribute(lambda o: o.amount_exclude_vat * Decimal("1.20"))  # Assuming 20% VAT
    organization_code = factory.Faker("ean13")
    course_code = factory.Faker("ean13")
    course_id = factory.Faker("uuid4")
