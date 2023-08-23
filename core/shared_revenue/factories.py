import factory
from factory.django import DjangoModelFactory

from core.organization.factories import OrganizationFactory

from .models import PartnershipLevel, RevenueConfiguration, ShareExecution


class PartnershipLevelFactory(DjangoModelFactory):
    class Meta:
        model = PartnershipLevel

    name = factory.Faker("word")
    description = factory.Faker("sentence")
    percentage = factory.Faker("pydecimal", left_digits=1, right_digits=2)


class RevenueConfigurationFactory(DjangoModelFactory):
    class Meta:
        model = RevenueConfiguration

    organization = factory.SubFactory(OrganizationFactory)
    partnership_level = factory.SubFactory(PartnershipLevelFactory)
    course_code = factory.Faker("word")
    start_date = factory.Faker("date_time_this_month")
    end_date = factory.Faker("date_time_this_month")


class ShareExecutionFactory(DjangoModelFactory):
    class Meta:
        model = ShareExecution

    organization = factory.SubFactory(OrganizationFactory)
    revenue_configuration = factory.SubFactory(RevenueConfigurationFactory)
    percentage = factory.Faker("pydecimal", left_digits=2, right_digits=2)
    value = factory.Faker("pydecimal", left_digits=2, right_digits=2)
    receipt = factory.Faker("word")
    executed = factory.Faker("boolean")
    response_payload = factory.Faker("pydict")
