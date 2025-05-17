#!/bin/bash

set -e

IMAGE_TAG="$1"
REPO="ghcr.io/michadebayo/assuraimant-web-app"

# Optionally pass in a different repo/tag via ENV vars if needed
COMMIT_SHA=${GITHUB_SHA:-$IMAGE_TAG}
BUILD_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "🛠 Building Docker image: $REPO:$IMAGE_TAG"
echo "🔢 Commit SHA: $COMMIT_SHA"
echo "⏰ Build Time: $BUILD_TIME"

docker-compose build \
  --build-arg COMMIT_SHA="$COMMIT_SHA" \
  --build-arg BUILD_TIME="$BUILD_TIME"

echo "✅ Docker image built: $REPO:$IMAGE_TAG"
