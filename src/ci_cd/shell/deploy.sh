#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Log in to GitHub Container Registry
echo "Logging into GitHub Container Registry..."
echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_ACTOR" --password-stdin

# Debugging output
echo "Using REPO_LC=${REPO_LC}"
echo "Using IMAGE_TAG=${IMAGE_TAG}"
echo "Using DATABASE_URL=${DATABASE_URL}"
echo "Using SECRET_KEY=${SECRET_KEY}"
echo "Using RENDER_API_TOKEN: ${ secrets.RENDER_API_TOKEN }"

# Validate required environment variables
if [[ -z "$REPO_LC" || -z "$IMAGE_TAG" || -z "$RENDER_API_TOKEN" || -z "$DATABASE_URL" || -z "$SECRET_KEY" ]]; then
  echo "❌ One or more required environment variables are not set. Exiting..."
  exit 1
fi

# Pull the Docker image from GHCR
echo "Pulling Docker image from GitHub Container Registry..."
docker pull ghcr.io/${REPO_LC}/assuraimant-web-app:${IMAGE_TAG}

# Deploy to Render
echo "Deploying Docker image to Render..."
RESPONSE=$(curl -s -o response_body.txt -w "%{http_code}" -X POST https://api.render.com/v1/services \
  -H "Authorization: Bearer $RENDER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "serviceName": "assuraimant-web-app",
        "image": "ghcr.io/'${REPO_LC}'/assuraimant-web-app:'"${IMAGE_TAG}"'",
        "env": "docker",
        "instanceCount": 1,
        "envVars": [
          {"key": "DATABASE_URL", "value": "'"$DATABASE_URL"'"},
          {"key": "SECRET_KEY", "value": "'"$SECRET_KEY"'"}
        ]
      }')

HTTP_STATUS=$(cat response_body.txt | tail -n 1)
RESPONSE_BODY=$(cat response_body.txt | head -n -1)

if [[ "$HTTP_STATUS" -ne 200 ]]; then
  echo "❌ Deployment failed with status code $HTTP_STATUS"
  echo "Response: $RESPONSE_BODY"
  exit 1
fi

echo "✅ Deployment to Render completed successfully!"