import factory
from factory.django import DjangoModelFactory
from faker.providers.date_time import Provider as DateProvider

from apps.organization.factories import OrganizationFactory
from apps.shared_revenue.models import PartnershipLevel, RevenueConfiguration, ShareExecution


class PartnershipLevelFactory(DjangoModelFactory):
    class Meta:
        model = PartnershipLevel
        django_get_or_create = ("name", "percentage")

    name = factory.Faker("word")
    description = factory.Faker("sentence")
    percentage = factory.Faker("pydecimal", left_digits=1, right_digits=2)


class RevenueConfigurationFactory(DjangoModelFactory):
    class Meta:
        model = RevenueConfiguration

    organization = factory.SubFactory(OrganizationFactory)
    partnership_level = factory.SubFactory(PartnershipLevelFactory)
    course_code = factory.Faker("word")
    start_date = factory.Faker(provider=DateProvider)
    end_date = factory.Faker(provider=DateProvider)


class ShareExecutionFactory(DjangoModelFactory):
    class Meta:
        model = ShareExecution

    organization = factory.SubFactory(OrganizationFactory)
    revenue_configuration = None
    percentage = factory.Faker("pydecimal", left_digits=2, right_digits=2)
    value = factory.Faker("pydecimal", left_digits=2, right_digits=2)
    receipt = factory.Faker("word")
    executed = factory.Faker("boolean")
    response_payload = factory.Faker("pydict")
