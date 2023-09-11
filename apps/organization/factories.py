import random

import factory
from factory.django import DjangoModelFactory

from apps.organization.models import Organization, OrganizationAddress, OrganizationContact
from apps.util.constants import ADDRESS_TYPES, CONTACT_TYPES


class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization

    def __select_vat_by_country(self):
        return {
            "PT": f"PT{random.randint(100000000, 999999999)}",
            "ES": f"ES{random.randint(100000000, 999999999)}",
            "IT": f"IT{random.randint(10000000000, 99999999999)}",
            "FR": f"FR{random.randint(10000000000, 99999999999)}",
            "DE": f"DE{random.randint(100000000, 999999999)}",
        }[self.vat_country]

    name = factory.Sequence(lambda n: f"Organization {n}")
    short_name = factory.Sequence(lambda n: f"Org {n}")
    slug = factory.Sequence(lambda n: f"org-{n}")
    iban = factory.Faker("iban")
    vat_country = factory.Iterator(["PT", "ES", "IT", "FR", "DE"])

    @factory.lazy_attribute
    def vat_number(self):
        return self.__select_vat_by_country()


class OrganizationAddressFactory(DjangoModelFactory):
    class Meta:
        model = OrganizationAddress

    organization = factory.SubFactory(OrganizationFactory)
    address_type = factory.Iterator(ADDRESS_TYPES)
    street = factory.Faker("street_address")
    postal_code = factory.Faker("postcode")
    city = factory.Faker("city")
    district = factory.Faker("state")
    country = factory.SelfAttribute("organization.vat_country")


class OrganizationContactFactory(DjangoModelFactory):
    class Meta:
        model = OrganizationContact

    organization = factory.SubFactory(OrganizationFactory)
    contact_type = factory.Iterator(CONTACT_TYPES)
    contact_value = factory.LazyAttribute(lambda _: factory.Factory("phone_number"))
    description = factory.Faker("text", max_nb_chars=255)
    is_main = False
