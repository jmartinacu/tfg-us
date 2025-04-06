from samer.settings.base import *  # noqa
from samer.utils import get_tuple_list_env

DEBUG = False

ADMINS = get_tuple_list_env(os.getenv("ADMINS"))  # noqa

ALLOWED_HOSTS = ["*"]

SECRET_KEY = os.getenv(  # noqa
    "SECRET_KEY",
    "django-insecure-lifiv!v&qwh$j*5$0cz#iizeesc7vf(y$eofl5u!y-82sb(^6n",
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB", "samer"),  # noqa
        "USER": os.getenv("POSTGRES_USER", "postgres"),  # noqa
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),  # noqa
        "HOST": os.getenv("POSTGRES_HOST", "127.0.0.1"),  # noqa
        "PORT": "5432",
    }
}

# SSL/TLS

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CSRF_TRUSTED_ORIGINS = ["https://samervalme.duckdns.org"]

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True
