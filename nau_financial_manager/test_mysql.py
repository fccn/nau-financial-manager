from .settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "test_nau_db",
        "USER": get_env_setting("MYSQL_ROOT_USER", "root"),
        "PASSWORD": get_env_setting("MYSQL_PASSWORD", "nau_password"),
        # Default mode it the development mode without docker
        "HOST": get_env_setting("DB_HOST", "127.0.0.1"),
        "PORT": get_env_setting("DB_PORT", 3306),
    },
}