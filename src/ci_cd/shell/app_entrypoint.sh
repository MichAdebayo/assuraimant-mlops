#!/bin/bash

set -e

GUNICORN_PORT=${GUNICORN_PORT:-8000}

echo "Waiting for database to be ready..."
until python manage.py showmigrations &>/dev/null; do
  echo "Database not ready, retrying in 3s..."
  sleep 3
done

echo "Running database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput || { echo "❌ Collectstatic failed"; exit 1; }

echo "Starting the application on port $GUNICORN_PORT..."
gunicorn brief_app.wsgi:application --bind 0.0.0.0:$GUNICORN_PORT --access-logfile -
