# Docker Build Troubleshooting Guide

## Issue: TLS Handshake Timeout / Network Errors

The error you're seeing:
```
failed to do request: Head "https://registry-1.docker.io/v2/library/node/manifests/18-alpine": 
net/http: TLS handshake timeout
```

This indicates Docker can't reach Docker Hub to download base images.

## Solutions (Try in Order)

### Solution 1: Check Docker Daemon and Restart
```bash
# Check if Docker is running
docker info

# Restart Docker Desktop
# On Mac: Click Docker icon in menu bar → Restart

# Or restart via command line
killall Docker && open /Applications/Docker.app
```

### Solution 2: Configure Docker DNS
Docker might be having DNS resolution issues.

```bash
# Edit Docker daemon config
# On Mac: Docker Desktop → Settings → Docker Engine

# Add this to the JSON config:
{
  "dns": ["8.8.8.8", "8.8.4.4"]
}

# Click "Apply & Restart"
```

### Solution 3: Use Docker Hub Mirror (For Slow/Blocked Connections)
If you're in a region with slow Docker Hub access:

```bash
# Edit Docker daemon config
# Add registry mirrors:
{
  "registry-mirrors": [
    "https://mirror.gcr.io"
  ],
  "dns": ["8.8.8.8", "8.8.4.4"]
}
```

### Solution 4: Increase Timeout
```bash
# Edit Docker daemon config
{
  "max-concurrent-downloads": 3,
  "max-concurrent-uploads": 5,
  "dns": ["8.8.8.8", "8.8.4.4"]
}
```

### Solution 5: Check Network/Firewall
```bash
# Test connectivity to Docker Hub
curl -I https://registry-1.docker.io/v2/

# Should return: HTTP/2 401 (unauthorized is OK, means it's reachable)

# If this fails, check:
# 1. VPN/Proxy settings
# 2. Corporate firewall
# 3. Internet connection
```

### Solution 6: Use VPN or Change Network
If you're on a restricted network:
- Try a different WiFi network
- Use mobile hotspot
- Use a VPN
- Disable any corporate proxy

### Solution 7: Pull Images Manually First
```bash
# Pull images one at a time with retries
docker pull python:3.11-slim
docker pull node:18-alpine
docker pull nginx:alpine

# Then try building again
docker-compose up --build
```

### Solution 8: Build with Retry Script
Create a retry script:

```bash
#!/bin/bash
# save as build-with-retry.sh

MAX_RETRIES=3
RETRY_COUNT=0

until docker-compose up --build -d || [ $RETRY_COUNT -eq $MAX_RETRIES ]; do
  RETRY_COUNT=$((RETRY_COUNT+1))
  echo "Build failed. Retry $RETRY_COUNT of $MAX_RETRIES..."
  sleep 5
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
  echo "Build failed after $MAX_RETRIES attempts"
  exit 1
fi
```

Run it:
```bash
chmod +x build-with-retry.sh
./build-with-retry.sh
```

## Quick Fix Commands

### Clean Docker and Retry
```bash
# Stop all containers
docker-compose down

# Clean Docker cache
docker system prune -a --volumes

# Restart Docker Desktop
# Then try again
docker-compose up --build
```

### Build with Verbose Output
```bash
# See detailed error messages
docker-compose up --build --progress=plain
```

### Build Services Separately
```bash
# Build backend only
docker-compose build backend

# Build frontend only
docker-compose build frontend

# Then start
docker-compose up -d
```

## Alternative: Build Without Cache
```bash
# Force rebuild without using cache
docker-compose build --no-cache
docker-compose up -d
```

## Check Docker Configuration

### View Current Docker Settings
```bash
# Check Docker info
docker info

# Check Docker version
docker --version
docker-compose --version
```

### Recommended Docker Desktop Settings
- **Memory**: 4GB minimum (8GB recommended)
- **CPUs**: 2 minimum (4 recommended)
- **Disk**: 20GB minimum

## If All Else Fails: Use Pre-built Images

Instead of building locally, you can:

1. **Build on a different machine** with better connectivity
2. **Use GitHub Actions** to build and push to Docker Hub
3. **Deploy directly to Railway/Render** (they build in the cloud)

## Network-Specific Issues

### Behind Corporate Proxy
Add to Docker daemon config:
```json
{
  "proxies": {
    "http-proxy": "http://proxy.example.com:8080",
    "https-proxy": "http://proxy.example.com:8080",
    "no-proxy": "localhost,127.0.0.1"
  }
}
```

### Using VPN
Some VPNs block Docker Hub:
- Try disabling VPN temporarily
- Or configure VPN to allow Docker Hub access

## Verification Steps

After applying fixes:

```bash
# 1. Test Docker connectivity
docker run hello-world

# 2. Test image pull
docker pull alpine

# 3. Build your project
docker-compose up --build

# 4. Check running containers
docker-compose ps

# 5. View logs
docker-compose logs -f
```

## Common Error Messages and Fixes

| Error | Solution |
|-------|----------|
| `TLS handshake timeout` | DNS/Network issue - try Solutions 1-3 |
| `connection refused` | Docker daemon not running - restart Docker |
| `no space left on device` | Clean Docker: `docker system prune -a` |
| `manifest unknown` | Wrong image name or version |
| `pull access denied` | Image doesn't exist or needs authentication |

## Still Having Issues?

If network problems persist, **deploy directly to cloud**:

```bash
# Skip local Docker build entirely
# Push code to GitHub
git add .
git commit -m "Ready for deployment"
git push

# Deploy on Railway/Render (they build in cloud)
# No local Docker build needed!
```

This bypasses your local network issues completely.
