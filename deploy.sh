#!/bin/bash

set -e

python manage.py migrate --noinput

python manage.py collectstatic --noinput

DEPLOY_STATUS="dev"
if [ -n "${DJANGO_SETTINGS_MODULE}" ]; then
    case "${DJANGO_SETTINGS_MODULE}" in
        "samer.settings.local")
            DEPLOY_STATUS="dev"
            ;;
        "samer.settings.prod")
            DEPLOY_STATUS="prod"
            ;;
        *)
            echo "Unknown DJANGO_SETTINGS_MODULE: ${DJANGO_SETTINGS_MODULE}"
            exit 1
            ;;
    esac
fi

if [ "${DEPLOY_STATUS}" == "dev" ]; then
    echo "Running in development mode"
    exec python manage.py runserver 0.0.0.0:8000
elif [ "${DEPLOY_STATUS}" == "prod" ]; then
    echo "Running in production mode"
    exec gunicorn samer.wsgi:application --bind 0.0.0.0:8000
fi