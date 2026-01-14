# Docker Deployment Guide

## Overview
This guide explains how to deploy the Dark Circles Detection application using Docker. The application consists of two services:
- **Backend**: FastAPI service running the YOLO model
- **Frontend**: React application served by Nginx

## Prerequisites
- Docker installed (version 20.10+)
- Docker Compose installed (version 2.0+)
- At least 4GB of available RAM
- Model file (`best (7).pt`) in the root directory

## Quick Start

### 1. Build and Run with Docker Compose
```bash
# Build and start both services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### 2. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 3. Stop the Application
```bash
# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Individual Service Deployment

### Backend Only
```bash
# Build backend image
docker build -t dark-circles-backend .

# Run backend container
docker run -p 8000:8000 dark-circles-backend
```

### Frontend Only
```bash
# Build frontend image
cd frontend
docker build -t dark-circles-frontend .

# Run frontend container
docker run -p 3000:80 dark-circles-frontend
```

## Memory Optimization

The cleaned `requirements.txt` now contains only essential packages:
- **Before**: 169 packages (~2GB+ when installed)
- **After**: 16 packages (~1.5GB when installed)

### Removed Unused Packages:
- Streamlit and related packages
- Firebase/Google Cloud services
- Database connectors (MySQL, PostgreSQL)
- Jupyter notebook dependencies
- AWS/S3 libraries
- Typesense
- Unnecessary data processing libraries

## Production Deployment

### Environment Variables
Create a `.env` file in the root directory:
```env
# Backend
PYTHONUNBUFFERED=1

# Frontend
REACT_APP_API_URL=http://your-backend-url:8000
```

### For Cloud Deployment (AWS, GCP, Azure)

#### Option 1: Docker Compose on VM
1. SSH into your VM
2. Clone the repository
3. Run `docker-compose up -d`

#### Option 2: Container Services
- **AWS ECS/Fargate**: Use the Dockerfiles to create task definitions
- **Google Cloud Run**: Deploy each service separately
- **Azure Container Instances**: Use docker-compose or individual containers

### For Netlify (Not Recommended for Backend)
⚠️ **Important**: Netlify is designed for static sites and serverless functions. The backend with YOLO model is too large for Netlify.

**Recommended Approach**:
1. Deploy backend on a container service (AWS ECS, Google Cloud Run, Railway, Render)
2. Deploy frontend on Netlify
3. Update `REACT_APP_API_URL` to point to your backend URL

## Troubleshooting

### Out of Memory Errors
1. **Increase Docker Memory Limit**:
   - Docker Desktop → Settings → Resources → Memory (set to 4GB+)

2. **Use Smaller Base Image**:
   - Already using `python:3.11-slim` (smallest official Python image)

3. **Optimize Model Loading**:
   - Model is loaded once at startup, not per request

### CORS Issues
The backend is configured to accept requests from:
- `http://localhost:3000` (development)
- `http://localhost` (production)
- All origins (`*`) for Docker deployment

Update `main.py` CORS settings if deploying to a specific domain.

### Model Loading Issues
If the model fails to load:
1. Ensure `best (7).pt` is in the root directory
2. Check Docker logs: `docker-compose logs backend`
3. Verify PyTorch/Ultralytics compatibility

## Health Checks

### Backend Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_path": "/app/best (7).pt"
}
```

### Frontend Health
```bash
curl http://localhost:3000
```

Should return the HTML of the React app.

## Scaling

### Horizontal Scaling
```yaml
# In docker-compose.yml
services:
  backend:
    deploy:
      replicas: 3
```

### Load Balancing
Add Nginx as a reverse proxy:
```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    depends_on:
      - backend
      - frontend
```

## Monitoring

### View Logs
```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

### Container Stats
```bash
docker stats
```

## Backup and Restore

### Backup Model
```bash
docker cp dark-circles-backend:/app/best\ \(7\).pt ./backup/
```

### Update Model
```bash
# Stop services
docker-compose down

# Replace model file
cp new-model.pt "best (7).pt"

# Rebuild and restart
docker-compose up --build -d
```

## Security Best Practices

1. **Don't expose unnecessary ports**
2. **Use environment variables for sensitive data**
3. **Keep Docker images updated**
4. **Scan images for vulnerabilities**:
   ```bash
   docker scan dark-circles-backend
   ```

## Cost Optimization

### Recommended Services for Budget Deployment:
1. **Railway.app** - Free tier, easy Docker deployment
2. **Render.com** - Free tier for web services
3. **Fly.io** - Free tier with Docker support
4. **Google Cloud Run** - Pay per use, generous free tier

## Support

For issues:
1. Check logs: `docker-compose logs`
2. Verify system requirements
3. Ensure all files are present
4. Check Docker daemon is running
