import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from apps.shared_revenue.models import RevenueConfiguration


class RevenueConfigurationFactory(DjangoModelFactory):
    class Meta:
        model = RevenueConfiguration

    organization = None
    partner_percentage = 0.70
    product_id = factory.Faker(
        "pystr_format",
        string_format="course-v%:?????+CBN???F+2023_T3",
    )
    start_date = factory.Faker(
        "date_time_between", start_date="-10d", end_date="+30d", tzinfo=timezone.get_current_timezone()
    )
    end_date = factory.Faker(
        "date_time_between", start_date="+40d", end_date="+70d", tzinfo=timezone.get_current_timezone()
    )
