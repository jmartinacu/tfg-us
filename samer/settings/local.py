from samer.settings.base import *  # noqa

DEBUG = True

ALLOWED_HOSTS = ["*"]

SECRET_KEY = (
    "django-insecure-lifiv!v&qwh$j*5$0cz#iizeesc7vf(y$eofl5u!y-82sb(^6n"  # noqa
)


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "samer"),  # noqa
        "USER": os.getenv("POSTGRES_USER", "postgres"),  # noqa
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),  # noqa
        "HOST": os.getenv("POSTGRES_HOST", ""),  # noqa
        "PORT": "5432",
    }
}
