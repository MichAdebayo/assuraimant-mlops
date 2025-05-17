#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Ensure all required variables are set early
if [[ -z "$GITHUB_TOKEN" || -z "$GITHUB_ACTOR" || -z "$REPO_LC" || -z "$IMAGE_TAG" || -z "$RENDER_API_TOKEN" ]]; then
  echo "❌ One or more required environment variables (GITHUB_TOKEN, GITHUB_ACTOR, REPO_LC, IMAGE_TAG, RENDER_API_TOKEN) are not set."
  exit 1
fi

# Log in to GitHub Container Registry
echo "🔐 Logging into GitHub Container Registry..."
echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_ACTOR" --password-stdin

# Debug Render API Token (partial only for security)
echo "🔑 RENDER_API_TOKEN starts with: ${RENDER_API_TOKEN:0:4}***"

# Pull the Docker image from GHCR
IMAGE="ghcr.io/${REPO_LC}/assuraimant-web-app:${IMAGE_TAG}"
echo "📥 Pulling Docker image: $IMAGE"
docker pull "$IMAGE"

# Deploy to Render
echo "🚀 Deploying Docker image to Render..."
echo "Deploying image: $IMAGE"
docker inspect "$IMAGE" --format='Image ID: {{.Id}}'

# Replace with your actual Render service ID
SERVICE_ID="srv-d0k6j0d6ubrc73b0uh0g"

if [[ -z "$SERVICE_ID" ]]; then
  echo "❌ SERVICE_ID is not set."
  exit 1
fi

# Prepare JSON payload
# DEPLOY_PAYLOAD=$(jq -n --arg image "$IMAGE" '{ image: $image }')

# # Prepare JSON payload with explicit version
# DEPLOY_PAYLOAD=$(jq -n \
#   --arg image "ghcr.io/${REPO_LC}/assuraimant-web-app:${IMAGE_TAG}" \
#   '{
#     dockerCommand: null,
#     imageUrl: $image,
#     isDockerCompose: false
#   }')

DEPLOY_PAYLOAD=$(jq -n \
  --arg image "ghcr.io/${REPO_LC}/assuraimant-web-app:${IMAGE_TAG}" \
  '{
    imageUrl: $image
    isDockerCompose: true
  }')

echo "🧾 Generated JSON Payload:"
echo "$DEPLOY_PAYLOAD" | jq .

# Send deploy request to Render
RESPONSE=$(curl -s -w "\n%{http_code}" "https://api.render.com/v1/services/${SERVICE_ID}/deploys" \
  -H "Authorization: Bearer $RENDER_API_TOKEN" \
  -H "Content-Type: application/json" \
  # --data "$DEPLOY_PAYLOAD")
  --data-binary "$DEPLOY_PAYLOAD" 2>&1)

# Parse response and HTTP status
HTTP_STATUS=$(echo "$RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$RESPONSE" | sed '$d')

if [[ "$HTTP_STATUS" != "200" && "$HTTP_STATUS" != "201" && "$HTTP_STATUS" != "202" ]]; then
  echo "❌ Deployment failed with status code $HTTP_STATUS"
  echo "📦 Response: $RESPONSE_BODY"
  exit 1
fi

  echo "✅ Deployment to Render completed successfully!"



# #!/bin/bash

# # Exit immediately if a command exits with a non-zero status
# set -e

# # Log in to GitHub Container Registry
# echo "Logging into GitHub Container Registry..."
# echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_ACTOR" --password-stdin

# # Debug Render API Token
# echo "RENDER_API_TOKEN is ${RENDER_API_TOKEN:0:4}***"

# # Validate required environment variables
# if [[ -z "$REPO_LC" || -z "$IMAGE_TAG" || -z "$RENDER_API_TOKEN" ]]; then
#   echo "❌ One or more required environment variables are not set. Exiting..."
#   exit 1
# fi

# # Pull the Docker image from GHCR
# echo "Pulling Docker image from GitHub Container Registry..."
# docker pull ghcr.io/${REPO_LC}/assuraimant-web-app:${IMAGE_TAG}

# # Deploy to Render
# echo "Deploying Docker image to Render..."

# # Enter service ID from the Render dashboard
# SERVICE_ID="srv-d0jgfjemcj7s73801ik0"

# # Verify service ID is accessible
# echo "SERVICE_ID = $SERVICE_ID"

# DEPLOY_PAYLOAD=$(jq -n \
#   --arg image "ghcr.io/${REPO_LC}/assuraimant-web-app:${IMAGE_TAG}" \
#   '{
#     image: $image
#   }')

# echo "Generated JSON Payload:"
# echo "$DEPLOY_PAYLOAD" | jq .

# RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "https://api.render.com/v1/services/${SERVICE_ID}/deploys" \
#   -H "Authorization: Bearer $RENDER_API_TOKEN" \
#   -H "Content-Type: application/json" \
#   --data-binary "$DEPLOY_PAYLOAD")

# # Split response and status code
# HTTP_STATUS=$(echo "$RESPONSE" | tail -n1)
# RESPONSE_BODY=$(echo "$RESPONSE" | head -n -1)

# echo "Deploying image: ghcr.io/${REPO_LC}/assuraimant-web-app:${IMAGE_TAG}"

# if [[ "$HTTP_STATUS" != "200" && "$HTTP_STATUS" != "201" ]]; then
#   echo "❌ Deployment failed with status code $HTTP_STATUS"
#   echo "Response: $RESPONSE_BODY"
#   exit 1
# fi

# echo "✅ Deployment to Render completed successfully!"
