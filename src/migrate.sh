#!/bin/bash

set -e

# Paramètres
DB_HOST=${MYSQL_HOST}
DB_PORT=${MYSQL_PORT}
SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"theai00tester@gmail.com"}

cd /app/

# Attente de la disponibilité de MySQL
echo "Waiting for MySQL at $DB_HOST..."
until nc -z "$DB_HOST" $DB_PORT; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "MySQL is up - proceeding"

# Appliquer les migrations
echo "Applying Django migrations..."
# /opt/venv/bin/python manage.py makemigrations --noinput
/opt/venv/bin/python manage.py migrate --noinput

# Créer le superutilisateur si nécessaire
echo "Creating superuser if necessary..."
/opt/venv/bin/python manage.py createsuperuser --noinput --email $SUPERUSER_EMAIL || true