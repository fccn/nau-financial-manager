import random

import factory
from factory.django import DjangoModelFactory

from apps.organization.models import Organization, OrganizationAddress, OrganizationContact
from apps.util.constants import ADDRESS_TYPES, CONTACT_TYPES


class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization
        django_get_or_create = ("short_name",)

    name = factory.Sequence(lambda n: f"Organization {n}")
    short_name = factory.Sequence(lambda n: f"Org {n}")
    iban = factory.Faker("iban")
    vat_country = factory.Iterator(["PT", "ES", "IT", "FR", "DE"])

    @factory.lazy_attribute
    def vat_number(self):
        return {
            "PT": f"{random.randint(100000000, 999999999)}",
            "ES": f"{random.randint(100000000, 999999999)}",
            "IT": f"{random.randint(10000000000, 99999999999)}",
            "FR": f"{random.randint(10000000000, 99999999999)}",
            "DE": f"{random.randint(100000000, 999999999)}",
        }[self.vat_country]


class OrganizationAddressFactory(DjangoModelFactory):
    class Meta:
        model = OrganizationAddress

    organization = factory.SubFactory(OrganizationFactory)
    street = factory.Faker("street_address")
    postal_code = factory.Faker("postcode")
    city = factory.Faker("city")
    district = factory.Faker("state")
    country = factory.SelfAttribute("organization.vat_country")

    @factory.lazy_attribute
    def address_type(self):
        return ADDRESS_TYPES[random.randint(0, 2)][0]


class OrganizationContactFactory(DjangoModelFactory):
    class Meta:
        model = OrganizationContact

    organization = factory.SubFactory(OrganizationFactory)
    description = factory.Faker("text", max_nb_chars=255)
    is_main = False
    contact_type = CONTACT_TYPES[random.randint(0, 2)][0]

    @factory.lazy_attribute
    def contact_value(self):
        country = self.organization.vat_country
        if self.contact_type == "email":
            return f"email{random.randint(1000, 9999)}@gmail.com"
        phone_number: str = factory.faker.faker.Faker(f"{country.code.lower()}_{country}").phone_number()

        return phone_number.replace(" ", "")[-9:]
