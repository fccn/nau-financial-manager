import factory
from factory.django import DjangoModelFactory

from apps.organization.models import Organization, OrganizationAddress, OrganizationContact
from apps.util.constants import ADDRESS_TYPES, CONTACT_TYPES, EUROPE_COUNTRIES


class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Sequence(lambda n: f"Organization {n}")
    short_name = factory.Sequence(lambda n: f"Org {n}")
    slug = factory.Sequence(lambda n: f"org-{n}")
    vat_country = factory.Iterator(EUROPE_COUNTRIES)
    vat_number = factory.Faker("random_number", digits=9)
    iban = factory.Faker("iban")


class OrganizationAddressFactory(DjangoModelFactory):
    class Meta:
        model = OrganizationAddress

    organization = factory.SubFactory(OrganizationFactory)
    address_type = factory.Iterator(ADDRESS_TYPES)
    street = factory.Faker("street_address")
    postal_code = factory.Faker("postcode")
    city = factory.Faker("city")
    district = factory.Faker("state")
    country = factory.Iterator(EUROPE_COUNTRIES)


class OrganizationContactFactory(DjangoModelFactory):
    class Meta:
        model = OrganizationContact

    organization = factory.SubFactory(OrganizationFactory)
    contact_type = factory.Iterator(CONTACT_TYPES)
    contact_value = factory.LazyAttribute(lambda _: factory.Factory("phone_number"))
    description = factory.Faker("text", max_nb_chars=255)
    is_main = False
