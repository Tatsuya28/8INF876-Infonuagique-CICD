#!/bin/bash

SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"theai00tester@gmail.com"}
cd /app/

/opt/venv/bin/python manage.py migrate --noinput # Apply database migrations
/opt/venv/bin/python manage.py createsuperuser --noinput --email $SUPERUSER_EMAIL || true # Create superuser if not exists