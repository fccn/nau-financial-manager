import factory
from factory.django import DjangoModelFactory

from apps.organization.models import Organization


class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization
        django_get_or_create = ("short_name",)

    name = factory.Sequence(lambda n: f"Organization {n}")
    short_name = factory.Sequence(lambda n: f"Org {n}")
    email = factory.Faker("email")
