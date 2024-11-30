#!/bin/bash

APP_PORT=${APP_PORT:-8000}
cd /app/
/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm django_cicd.wsgi:application --bind "0.0.0.0:${APP_PORT}"