#!/usr/bin/env bash

set -ex

ENTRY="${1}.wsgi:application"
[[ -n "${2}" ]] && WORKERS="${2}" || WORKERS="4"
[[ -n "${3}" ]] && PORT="${3}" || PORT="9000"

python manage.py collectstatic --noinput

gunicorn ${ENTRY} --workers ${WORKERS} -b 0.0.0.0:${PORT}
