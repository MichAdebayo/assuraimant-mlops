#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Build Docker Compose image
echo "Building Docker Compose image..."
docker-compose build
