import random
import string

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from apps.organization.factories import OrganizationFactory
from apps.shared_revenue.models import RevenueConfiguration, ShareExecution


class RevenueConfigurationFactory(DjangoModelFactory):
    class Meta:
        model = RevenueConfiguration

    organization = None
    partner_percentage = 0.70
    product_id = (
        f"course-v1:UPorto+CBN{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}F+2023_T3"
    )
    start_date = factory.Faker(
        "date_time_between", start_date="now", end_date="+30d", tzinfo=timezone.get_current_timezone()
    )
    end_date = factory.Faker(
        "date_time_between", start_date="+40d", end_date="+70d", tzinfo=timezone.get_current_timezone()
    )


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
