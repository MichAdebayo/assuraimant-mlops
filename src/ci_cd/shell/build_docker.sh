#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

export IMAGE_TAG="$1"

# Build Docker Compose image
echo "Building Docker Compose image with IMAGE_TAG=$IMAGE_TAG..."
docker-compose -f [./src/ci_cd/docker/docker-compose.yml](VALID_FILE) build
