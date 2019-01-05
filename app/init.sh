#!/usr/bin/env bash

set -ex

if [ "$1" = "app" ];then
    python manage.py collectstatic --noinput
fi

shift

exec "$@"
