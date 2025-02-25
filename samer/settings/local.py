from samer.settings.base import *  # noqa

DEBUG = True

ALLOWED_HOSTS = ["*"]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (
    "django-insecure-lifiv!v&qwh$j*5$0cz#iizeesc7vf(y$eofl5u!y-82sb(^6n"  # noqa
)


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "samer"),  # noqa
        "USER": os.getenv("DB_USER", "postgres"),  # noqa
        "PASSWORD": os.getenv("DB_PASS", ""),  # noqa
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}
