from __future__ import absolute_import

import calendar
from datetime import datetime, timedelta

from celery import shared_task

from apps.shared_revenue.services.split_export import SplitExportService


@shared_task(name="apps.shared_revenue.tasks.excute_split_revenue_report")
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
