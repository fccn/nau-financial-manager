import factory
from factory.django import DjangoModelFactory

from apps.organization.factories import OrganizationFactory
from apps.shared_revenue.models import PartnershipLevel, RevenueConfiguration, ShareExecution
from apps.shared_revenue.serializers import RevenueConfigurationSerializer


class PartnershipLevelFactory(DjangoModelFactory):
    class Meta:
        model = PartnershipLevel
        django_get_or_create = ("percentage", "name")

    name = factory.Faker("word")
    description = factory.Faker("sentence")
    percentage = factory.Faker("pydecimal", left_digits=1, right_digits=2)


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

    @factory.lazy_attribute
    def revenue_configuration(self):
        partnership_level = PartnershipLevelFactory.create()
        return factory.DictFactory(
            **RevenueConfigurationSerializer(
                RevenueConfigurationFactory.create(partnership_level=partnership_level)
            ).data
        )
