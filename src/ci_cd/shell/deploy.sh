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
if [[ -z "$REPO_LC" || -z "$IMAGE_TAG" || -z "$RENDER_API_TOKEN" ]]; then
  echo "❌ One or more required environment variables are not set. Exiting..."
  exit 1
fi

# Pull the Docker image from GHCR
echo "Pulling Docker image from GitHub Container Registry..."
docker pull ghcr.io/${REPO_LC}/assuraimant-web-app:${IMAGE_TAG}

# Deploy to Render
echo "Deploying Docker image to Render..."

# Enter service ID from the Render dashboard
SERVICE_ID="srv-d0jgfjemcj7s73801ik0"

DEPLOY_PAYLOAD=$(jq -n \
  --arg image "ghcr.io/${REPO_LC}/assuraimant-web-app:${IMAGE_TAG}" \
  '{
    image: $image
  }')

echo "Generated JSON Payload:"
echo "$DEPLOY_PAYLOAD" | jq .

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "https://api.render.com/v1/services/${SERVICE_ID}/deploys" \
  -H "Authorization: Bearer $RENDER_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data-binary "$DEPLOY_PAYLOAD")

# Split response and status code
HTTP_STATUS=$(echo "$RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$RESPONSE" | head -n -1)

if [[ "$HTTP_STATUS" != "200" && "$HTTP_STATUS" != "201" ]]; then
  echo "❌ Deployment failed with status code $HTTP_STATUS"
  echo "Response: $RESPONSE_BODY"
  echo "✅ Deployment to Render completed successfully!"
  exit 1
fi
