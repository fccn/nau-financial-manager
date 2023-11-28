import calendar
import os
from datetime import datetime, timedelta

import django
from celery import Celery
from django.conf import settings

from apps.shared_revenue.services.split_export import SplitExportService

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nau_financial_manager.settings")
django.setup()


app = Celery("nau_financial_manager", backend="redis", broker="redis://nau-redis:6379")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task
def excute_split_revenue_report():
    now = datetime.now()
    _, last_day = calendar.monthrange(year=now.year, month=(now.month - 1))

    days_until_first_day = last_day + (now.day - 1)
    start_date = (
        (now - timedelta(days=days_until_first_day)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    )
    end_date = (now - timedelta(days=now.day)).replace(hour=23, minute=59, second=59, microsecond=59).isoformat()

    SplitExportService().export_split_to_xlsx(
        start_date=start_date,
        end_date=end_date,
    )
