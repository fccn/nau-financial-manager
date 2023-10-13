import factory
from factory.django import DjangoModelFactory

from apps.organization.factories import OrganizationFactory
from apps.shared_revenue.models import RevenueConfiguration, ShareExecution


class RevenueConfigurationFactory(DjangoModelFactory):
    class Meta:
        model = RevenueConfiguration

    organization = None
    partner_percentage = factory.Faker("pydecimal", min_value=0, max_value=1, left_digits=1, right_digits=2)
    course_code = None
    start_date = factory.Faker(provider="date_time")
    end_date = factory.Faker(provider="date_time")


class ShareExecutionFactory(DjangoModelFactory):
    class Meta:
        model = ShareExecution

    organization = factory.SubFactory(OrganizationFactory)
    percentage = factory.Faker("pydecimal", min_value=0, max_value=1, left_digits=1, right_digits=2)
    value = factory.Faker("pydecimal", min_value=0, max_value=500, left_digits=3, right_digits=2)
    receipt = factory.Faker("word")
    executed = factory.Faker("boolean")
    response_payload = factory.DictFactory()
    revenue_configuration = None
