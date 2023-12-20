"""
Django settings for nau_financial_manager project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import codecs
import copy
import logging.config
import os
from pathlib import Path

import yaml
from django.core.exceptions import ImproperlyConfigured


def get_env_setting(env_variable, default=None):
    """Get the environment variable value or return its default value."""
    try:
        return os.environ[env_variable]
    except KeyError:
        if default:
            return default
        else:
            error_msg = "Set the {} environment variable".format(env_variable)
            raise ImproperlyConfigured(error_msg)


CONFIG_FILE = get_env_setting("FINANCIAL_MANAGER_CFG", "./config.yml")

# Load the configuration from an YAML file and expose the configurations on a `CONFIG` object.
with codecs.open(CONFIG_FILE, encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)

    # Add the key/values from config into the global namespace of this module.
    __config_copy__ = copy.deepcopy(CONFIG)

    vars().update(__config_copy__)


BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = CONFIG.get("DEBUG", False)

# Optionally load the SECRET_KEY from the config.yml file or by environment variable.
# This allows us to run collectstatic without a special config.yml file or a specific
# static.py settings file.
SECRET_KEY = CONFIG.get("SECRET_KEY", get_env_setting("SECRET_KEY", "change-me"))
if SECRET_KEY == "change-me" and not DEBUG:
    raise ImproperlyConfigured("For security reasons you need to change the 'SECRET_KEY'.")

ALLOWED_HOSTS = CONFIG.get("ALLOWED_HOSTS", ["127.0.0.1", "localhost"])

STATIC_ROOT = os.path.join(get_env_setting("STATIC_ROOT", "./data/static"))

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
WSGI_APPLICATION = "nau_financial_manager.wsgi.application"

# The normal Django `DATABASES`` setting
DATABASES = CONFIG.get(
    "DATABASES",
    {
        "default": {
            # The DB_HOST needs to be overridden from environment variable because we have 2 modes
            # of running on the development mode, one from docker and another outside docker.
            # Each modes connects to MySQL host differently.
            "ENGINE": get_env_setting("ENGINE", "django.db.backends.mysql"),
            "NAME": get_env_setting("MYSQL_DATABASE", "nau_db"),
            "USER": get_env_setting("MYSQL_USER", "nau_user"),
            "PASSWORD": get_env_setting("MYSQL_PASSWORD", "nau_password"),
            # Default mode it the development mode without docker
            "HOST": get_env_setting("DB_HOST", "127.0.0.1"),
            "PORT": get_env_setting("DB_PORT", 3306),
        }
    },
)


# When it is running in dev environment, the used STORAGES is FileSystemStorage
# if it is running in prod environment, it uses the STORAGES located in the FINANCIAL_MANAGER_CFG variables
# which is a boto3 config implemented by django-storages package
STORAGES = CONFIG.get(
    "STORAGES",
    {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
            "OPTIONS": {
                "location": f"{BASE_DIR}/files",
                "base_url": f"{BASE_DIR}/files/",
            },
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    },
)

TEMPLATES = CONFIG.get(
    "TEMPLATES",
    [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [BASE_DIR / "templates"],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        }
    ],
)


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

# Celery settings
CELERY_APP = CONFIG.get("CELERY_APP", "nau_financial_manager")
CELERY_BROKER_URL = CONFIG.get("CELERY_BROKER_URL", "redis://nau-redis:6379/0")
CELERY_RESULT_BACKEND = CONFIG.get("CELERY_RESULT_BACKEND", "django-db")
CELERY_CACHE_BACKEND = CONFIG.get("CELERY_CACHE_BACKEND", "default")
CELERY_TASK_TRACK_STARTED = CONFIG.get("CELERY_TASK_TRACK_STARTED", True)
CELERY_ACCEPT_CONTENT = CONFIG.get("CELERY_ACCEPT_CONTENT", ["application/json"])
CELERY_TASK_SERIALIZER = CONFIG.get("CELERY_TASK_SERIALIZER", "json")
CELERY_RESULT_SERIALIZER = CONFIG.get("CELERY_RESULT_SERIALIZER", "json")
CELERY_RESULTS_EXTENDED = CONFIG.get("CELERY_RESULTS_EXTENDED", True)
CELERY_BEAT_SCHEDULER = CONFIG.get("CELERY_BEAT_SCHEDULER", "django_celery_beat.schedulers:DatabaseScheduler")
# WORKAROUND TO CELERY USING MYSQL
DJANGO_CELERY_RESULTS_TASK_ID_MAX_LENGTH = 191

# Django Cache settings
#
# By default it uses the Redis as Django Cache.
#
# The next configuration is used for development proposes.
# If you need to change this for a specific environment update the `CACHES` key
# on the `FINANCIAL_MANAGER_CFG` yaml file.
CACHES = CONFIG.get(
    "CACHES",
    {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": "redis://localhost:6379/0",
            "KEY_PREFIX": "naufm",
            "TIMEOUT": 60 * 15,  # in seconds: 60 * 15 (15 minutes)
        }
    },
)

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


LOGGING = CONFIG.get(
    "LOGGING",
    {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "error": {
                "level": "ERROR",
                "class": "logging.StreamHandler",
            },
            "warning": {
                "level": "WARNING",
                "class": "logging.StreamHandler",
            },
            "info": {
                "level": "INFO",
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["error", "warning", "info"],
                "level": 1,
                "propagate": True,
            },
            "nau_financial_manager": {
                "handlers": ["error", "warning", "info"],
                "level": 1,
                "propagate": True,
            },
        },
    },
)

LOGGING_CONFIG = None
logging.config.dictConfig(LOGGING)

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email configurations
EMAIL_SENDER = CONFIG.get("EMAIL_SENDER", "")
EMAIL_BACKEND = CONFIG.get("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = CONFIG.get("EMAIL_HOST", "")
EMAIL_PORT = CONFIG.get("EMAIL_PORT", "")
EMAIL_HOST_USER = CONFIG.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = CONFIG.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = CONFIG.get("EMAIL_USE_TLS", "")
EMAIL_USE_SSL = CONFIG.get("EMAIL_USE_SSL", "")
EMAIL_TIMEOUT = CONFIG.get("EMAIL_TIMEOUT", "")
EMAIL_SSL_KEYFILE = CONFIG.get("EMAIL_SSL_KEYFILE", "")
EMAIL_SSL_CERTFILE = CONFIG.get("EMAIL_SSL_CERTFILE", "")

# S3 file informations
FILE_PATH_LINK = CONFIG.get("FILE_PATH_LINK", "")

# Sage X3 - Transaction processor settings
TRANSACTION_PROCESSOR_URL = CONFIG.get("TRANSACTION_PROCESSOR_URL", "")
IVA_VACITM1_FIELD = CONFIG.get("IVA_VACITM1_FIELD", "NOR")
GEOGRAPHIC_ACTIVITY_VACBPR_FIELD = CONFIG.get("GEOGRAPHIC_ACTIVITY_VACBPR_FIELD", "CON")
USER_PROCESSOR_AUTH = CONFIG.get("USER_PROCESSOR_AUTH", "")
USER_PROCESSOR_PASSWORD = CONFIG.get("USER_PROCESSOR_PASSWORD", "")

# iLink - Receipt host information
RECEIPT_HOST_URL = CONFIG.get("RECEIPT_HOST_URL", "")
RECEIPT_ENTITY_PUBLIC_KEY = CONFIG.get("RECEIPT_ENTITY_PUBLIC_KEY", "")
RECEIPT_BEARER_TOKEN = CONFIG.get("RECEIPT_BEARER_TOKEN", "")

SWAGGER_PROJECT_NAME = CONFIG.get("SWAGGER_PROJECT_NAME", "Nau Financial Manager")
SWAGGER_PROJECT_VERSION = CONFIG.get("SWAGGER_PROJECT_VERSION", "1.0.0")
SWAGGER_DESCRIPTION = CONFIG.get("SWAGGER_DESCRIPTION", "API for Nau Financial Manager")

# Add a way to use Token authentication on the Swagger UI
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {"api_key": {"type": "apiKey", "in": "header", "name": "Authorization"}},
}
