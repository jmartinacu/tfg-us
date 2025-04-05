#!/bin/bash

if [[ -z "${DJANGO_SETTING}" ]]; then
  echo "DJANGO_SETTING environment variable is not set. Please set it to the desired settings module."
  exit 1
fi

python manage.py migrate --noinput --settings="${DJANGO_SETTING}"

python manage.py collectstatic --noinput --settings="${DJANGO_SETTING}"

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

LAUNCH_MODE=$(echo "${DJANGO_SETTING}" | cut -d '.' -f 3)

bash "${SCRIPT_DIR}/populate.sh" "${LAUNCH_MODE}"

python manage.py runserver 0.0.0.0:8000 --settings="${DJANGO_SETTING}"