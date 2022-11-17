#!/bin/bash
set -e

poetry run python manage.py migrate

#poetry run python manage.py compress
# Populate sitestatic directory. TODO: Do we need to cronjob this?
poetry run python manage.py collectstatic --no-input

exec poetry run gunicorn -b 0.0.0.0:8000 --log-file - -w 10 temba.wsgi
