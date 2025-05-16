#!/bin/bash

set -e

GUNICORN_PORT=${GUNICORN_PORT:-8000}

echo "Waiting for database to be ready..."
until python manage.py showmigrations &>/dev/null; do
  echo "Database not ready, retrying in 3s..."
  sleep 3
done

echo "Database is ready. Running database migrations..."
if ! python manage.py migrate; then
  echo "❌ Database migrations failed"
  exit 1
fi

echo "Collecting static files..."
if ! python manage.py collectstatic --noinput; then
  echo "❌ Collectstatic failed"
  exit 1
fi

echo "Starting the application on port $GUNICORN_PORT..."
exec gunicorn brief_app.wsgi:application --bind 0.0.0.0:$GUNICORN_PORT --access-logfile -
