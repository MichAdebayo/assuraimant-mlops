#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Run Django tests
echo "Running Django tests..."
python src/brief_app/manage.py test