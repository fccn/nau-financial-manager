"""
Django settings for nau_financial_manager project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from pathlib import Path

from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv(), default="localhost")

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "safedelete",
    "rest_framework",
    "django_filters",
    "rest_framework.authtoken",
    "drf_yasg",
    "auditlog",
    "celery",
    "django_countries",
    "django_celery_results",
    "django_celery_beat",
]

LOCAL_APPS = [
    "apps.billing",
    "apps.organization",
    "apps.shared_revenue",
    "apps.util",
]

INSTALLED_APPS = [*DJANGO_APPS, *THIRD_PARTY_APPS, *LOCAL_APPS]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "auditlog.middleware.AuditlogMiddleware",
]
AUTH_USER_MODEL = "util.CustomUser"
ROOT_URLCONF = "nau_financial_manager.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "nau_financial_manager.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("MYSQL_DATABASE"),
        "USER": config("MYSQL_USER_ROOT"),
        "PASSWORD": config("MYSQL_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "EXCEPTION_HANDLER": "apps.util.exceptions.custom_exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework.authentication.TokenAuthentication",),
    "DEFAULT_PAGINATION_CLASS": "apps.util.paginations.ShortResultsSetPagination",
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}

CELERY_APP = "nau_financial_manager"
CELERY_BROKER_URL = config("CELERY_BROKER_URL", "redis://nau-redis:6379/0")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", "django-db")
CELERY_CACHE_BACKEND = "default"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# WORKAROUND TO CELERY USING MYSQL
DJANGO_CELERY_RESULTS_TASK_ID_MAX_LENGTH = 191


RESDIS_URL = config("REDIS_URL", "redis://localhost:6379/")
REDIS_HOST = config("REDIS_HOST", "nau-redis")
REDIS_PORT = config("REDIS_PORT", 6379)
REDIS_DB = config("REDIS_DB", 0)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": config("REDIS_URL", "redis://localhost:6379/"),
        "KEY_PREFIX": "naufm",
        "TIMEOUT": 60 * 15,  # in seconds: 60 * 15 (15 minutes)
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Transcation processor settings
TRANSACTION_PROCESSOR_URL = ""
IVA_VACITM1_FIELD = "NOR"
GEOGRAPHIC_ACTIVITY_VACBPR_FIELD = "CON"
USER_PROCESSOR_AUTH = ""
USER_PROCESSOR_PASSWORD = ""
