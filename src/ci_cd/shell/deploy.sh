#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Log in to GitHub Container Registry
echo "Logging into GitHub Container Registry..."
echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_ACTOR" --password-stdin

# Pull the Docker image from GHCR
echo "Pulling Docker image from GitHub Container Registry..."
docker pull ghcr.io/${REPO_LC}/assuraimant-web-app:${IMAGE_TAG}

# Deploy to Render
echo "Deploying Docker image to Render..."

# Set Render environment variables if needed (e.g., token)
export RENDER_API_TOKEN="$RENDER_API_TOKEN"

# Deploy the app to Render using the Docker image
curl -X POST https://api.render.com/v1/services \
  -H "Authorization: Bearer $RENDER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "serviceName": "assuraimant-web-app",
        "image": "ghcr.io/'${REPO_LC}':latest",
        "env": "docker",
        "instanceCount": 1,
        "envVars": [
          {"key": "DATABASE_URL", "value": "'"$DATABASE_URL"'"},
          {"key": "SECRET_KEY", "value": "'"$SECRET_KEY"'"}
        ]
      }'

echo "Deployment to Render completed!"