import random
import string

import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from apps.shared_revenue.models import RevenueConfiguration


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
