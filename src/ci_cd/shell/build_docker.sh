#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Build Docker Compose image
echo "Building Docker Compose image..."
docker-compose -f ./src/ci_cd/docker/docker-compose.yml build

# Tag the Docker image
echo "Tagging Docker image..."
docker tag ghcr.io/${REPO_LC}/assuraimant-web-app:latest $IMAGE_NAME:$IMAGE_TAG