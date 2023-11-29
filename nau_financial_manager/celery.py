import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nau_financial_manager.settings")

app = Celery("nau_financial_manager", backend="redis", broker="redis://nau-redis:6379")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
