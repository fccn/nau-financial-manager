from decimal import Decimal

import factory

from apps.billing.models import Receipt, ReceiptItem
from apps.organization.factories import OrganizationFactory


class ReceiptFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Receipt

    name = factory.Faker("name")
    email = factory.Faker("email")
    address = factory.Faker("address")
    vat_identification_country = factory.Faker("country_code")
    vat_identification_number = factory.Faker("ssn")
    total_amount_exclude_vat = factory.Faker("pydecimal", left_digits=5, right_digits=2)

    receipt_link = factory.Faker("url")
    receipt_document_id = factory.Faker("uuid4")
    organization = factory.SubFactory(OrganizationFactory)

    # Assuming 20% VAT
    @factory.lazy_attribute
    def total_amount_include_vat(self):
        return self.total_amount_exclude_vat * Decimal("1.20")


class ReceiptItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReceiptItem

    receipt = factory.SubFactory(ReceiptFactory)
    description = factory.Faker("sentence")
    quantity = factory.Faker("pyint", min_value=1, max_value=10)
    vat_tax = factory.Faker("pydecimal", left_digits=3, right_digits=2)
    amount_exclude_vat = factory.Faker("pydecimal", left_digits=5, right_digits=2)
    organization_code = factory.Faker("ean13")
    course_code = factory.Faker("ean13")
    course_id = factory.Faker("uuid4")

    # Assuming 20% VAT
    @factory.lazy_attribute
    def amount_include_vat(self):
        return self.amount_exclude_vat * Decimal("1.20")
