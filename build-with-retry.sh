#!/bin/bash

# Docker Build Retry Script
# This script retries the Docker build if it fails due to network issues

MAX_RETRIES=3
RETRY_COUNT=0
WAIT_TIME=10

echo "🚀 Starting Docker build with retry logic..."
echo "Max retries: $MAX_RETRIES"
echo ""

until docker-compose up --build -d || [ $RETRY_COUNT -eq $MAX_RETRIES ]; do
  RETRY_COUNT=$((RETRY_COUNT+1))
  echo ""
  echo "❌ Build failed. Retry $RETRY_COUNT of $MAX_RETRIES..."
  echo "⏳ Waiting $WAIT_TIME seconds before retry..."
  sleep $WAIT_TIME
  
  # Clean up failed containers
  docker-compose down 2>/dev/null
  
  echo "🔄 Retrying build..."
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
  echo ""
  echo "❌ Build failed after $MAX_RETRIES attempts"
  echo ""
  echo "Troubleshooting steps:"
  echo "1. Check your internet connection"
  echo "2. Restart Docker Desktop"
  echo "3. Try: docker pull python:3.11-slim"
  echo "4. Try: docker pull node:18-alpine"
  echo "5. Check DOCKER_TROUBLESHOOTING.md for more solutions"
  exit 1
fi

echo ""
echo "✅ Build successful!"
echo ""
echo "🌐 Services are running:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo ""
echo "📊 View logs: docker-compose logs -f"
echo "🛑 Stop services: docker-compose down"
