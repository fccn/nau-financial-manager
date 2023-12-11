import os

from celery import Celery
from django.conf import settings

from nau_financial_manager.settings import CELERY_BROKER_URL

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nau_financial_manager.settings")

app = Celery("nau_financial_manager", backend="redis", broker=CELERY_BROKER_URL)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
