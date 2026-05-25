#!/bin/bash

# Script de build Docker pour BryShop
# Usage: ./build-docker.sh [version]

VERSION=${1:-latest}
IMAGE_NAME="bryshop"

echo "🐳 Building Docker image: $IMAGE_NAME:$VERSION"
echo "================================================"

# Build l'image
docker build \
  --tag $IMAGE_NAME:$VERSION \
  --tag $IMAGE_NAME:latest \
  --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
  --build-arg VCS_REF=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown") \
  .

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "📊 Image details:"
    docker images $IMAGE_NAME:$VERSION
    echo ""
    echo "🚀 To run the image:"
    echo "   docker-compose up -d"
    echo ""
    echo "   OR"
    echo ""
    echo "   docker run -d -p 8000:8000 --name bryshop_web $IMAGE_NAME:$VERSION"
else
    echo ""
    echo "❌ Build failed!"
    exit 1
fi
