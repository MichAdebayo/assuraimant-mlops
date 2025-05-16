#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Log in to GitHub Container Registry
echo "Logging into GitHub Container Registry..."
echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_ACTOR" --password-stdin

# Debugging output
# echo "Using REPO_LC=${REPO_LC}"
# echo "Using IMAGE_TAG=${IMAGE_TAG}"
# echo "Using DATABASE_URL=${DATABASE_URL}"
# echo "Using SECRET_KEY=${SECRET_KEY}"
# echo "Using RENDER_API_TOKEN: ${RENDER_API_TOKEN}"
# echo "GITHUB_ACTOR is: $GITHUB_ACTOR"

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

JSON_PAYLOAD=$(jq -n \
  --arg serviceName "assuraimant-web-app" \
  --arg image "ghcr.io/${REPO_LC}/assuraimant-web-app:${IMAGE_TAG}" \
  --arg env "docker" \
  --argjson instanceCount 1 \
  --arg db_url "$DATABASE_URL" \
  --arg secret "$SECRET_KEY" \
  '{
    serviceName: $serviceName,
    image: $image,
    env: $env,
    instanceCount: $instanceCount,
    envVars: [
      { key: "DATABASE_URL", value: $db_url },
      { key: "SECRET_KEY", value: $secret }
    ]
  }')

echo "$JSON_PAYLOAD" | jq .

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST https://api.render.com/v1/services \
  -H "Authorization: Bearer $RENDER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$JSON_PAYLOAD")

# Split response and status code
HTTP_STATUS=$(echo "$RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$RESPONSE" | head -n -1)

if [[ "$HTTP_STATUS" != "200" && "$HTTP_STATUS" != "201" ]]; then
  echo "❌ Deployment failed with status code $HTTP_STATUS"
  echo "Response: $RESPONSE_BODY"
  exit 1
fi

echo "✅ Deployment to Render completed successfully!"