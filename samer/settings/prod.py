from samer.settings.base import *  # noqa
from samer.utils import get_tuple_list_env

DEBUG = False

ADMINS = get_tuple_list_env(os.getenv("ADMINS"))  # noqa

ALLOWED_HOSTS = ["*"]

SECRET_KEY = os.getenv(  # noqa
    "SECRET_KEY",
    "django-insecure-lifiv!v&qwh$j*5$0cz#iizeesc7vf(y$eofl5u!y-82sb(^6n",
)

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("DB_NAME", "samer"),  # noqa
        "USER": os.getenv("DB_USER", "postgres"),  # noqa
        "PASSWORD": os.getenv("DB_PASS", ""),  # noqa
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

# SSL/TLS

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CSRF_TRUSTED_ORIGINS = ["https://samervalme.duckdns.org"]

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True
