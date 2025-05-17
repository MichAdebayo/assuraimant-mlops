#!/bin/bash

set -eo pipefail

GUNICORN_PORT=${GUNICORN_PORT:-8000}
MAX_RETRIES=120
RETRY_INTERVAL=3

echo "🚀 Starting Assuraimant Web App"
echo "🧾 Version Info:"
if [[ -f /app/version.txt ]]; then
  cat /app/version.txt
else
  echo "⚠️ version.txt not found"
fi

echo "DATABASE_URL is: $DATABASE_URL"

echo ""
echo "⏳ Waiting for database to be ready..."
COUNT=0
until python manage.py showmigrations &>/dev/null; do
  COUNT=$((COUNT + 1))
  if [ "$COUNT" -ge "$MAX_RETRIES" ]; then
    echo "⛔️ Database not ready after $MAX_RETRIES attempts, exiting..."
    exit 1
  fi
  echo "⛔️ Database not ready, retrying in ${RETRY_INTERVAL}s... ($COUNT/$MAX_RETRIES)"
  sleep $RETRY_INTERVAL
done

echo "✅ Database is ready. Running migrations..."
if ! python manage.py migrate; then
  echo "❌ Database migrations failed"
  exit 1
fi

echo "📦 Collecting static files..."
if ! python manage.py collectstatic --noinput; then
  echo "❌ Collectstatic failed"
  exit 1
fi

echo "🚀 Launching Gunicorn on port $GUNICORN_PORT..."
exec gunicorn brief_app.wsgi:application --bind 0.0.0.0:$GUNICORN_PORT --access-logfile -
