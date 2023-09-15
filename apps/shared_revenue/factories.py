import factory
from factory.django import DjangoModelFactory

from apps.organization.factories import OrganizationFactory
from apps.shared_revenue.models import PartnershipLevel, RevenueConfiguration, ShareExecution


class PartnershipLevelFactory(DjangoModelFactory):
    class Meta:
        model = PartnershipLevel
        django_get_or_create = (
            "percentage",
            "name",
        )

    name = factory.Faker("word")
    description = factory.Faker("sentence")
    percentage = factory.Faker("pydecimal", min_value=0, max_value=1, left_digits=1, right_digits=2)


class RevenueConfigurationFactory(DjangoModelFactory):
    class Meta:
        model = RevenueConfiguration

    organization = factory.SubFactory(OrganizationFactory)
    partnership_level = factory.SubFactory(PartnershipLevelFactory)
    course_code = None
    start_date = factory.Faker(provider="date_time")
    end_date = factory.Faker(provider="date_time")


class ShareExecutionFactory(DjangoModelFactory):
    class Meta:
        model = ShareExecution

    organization = factory.SubFactory(OrganizationFactory)
    percentage = factory.Faker("pydecimal", left_digits=2, right_digits=2)
    value = factory.Faker("pydecimal", left_digits=2, right_digits=2)
    receipt = factory.Faker("word")
    executed = factory.Faker("boolean")
    response_payload = factory.DictFactory()
    revenue_configuration = None
