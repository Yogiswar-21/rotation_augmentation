# Railway Deployment Guide

## Quick Deploy to Railway (Recommended)

Railway provides the easiest way to deploy both frontend and backend with a single unified URL.

### Prerequisites
- GitHub account
- Railway account (sign up at https://railway.app)
- Your code pushed to GitHub

### Method 1: Deploy via GitHub (Easiest)

1. **Push your code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/dark-circles-detection.git
   git push -u origin main
   ```

2. **Deploy on Railway**:
   - Go to https://railway.app
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway auto-detects the Dockerfile and docker-compose.yml

3. **Configure Services**:
   - Railway will create two services automatically (backend & frontend)
   - Click on backend service → Settings → Generate Domain
   - Click on frontend service → Settings → Generate Domain
   - Note the backend URL (e.g., `https://backend-production-xxxx.up.railway.app`)

4. **Update Frontend Environment**:
   - Go to frontend service → Variables
   - Add: `REACT_APP_API_URL` = `https://your-backend-url.up.railway.app`
   - Redeploy frontend

5. **Access Your App**:
   - Frontend: `https://frontend-production-xxxx.up.railway.app`
   - Backend: `https://backend-production-xxxx.up.railway.app`

### Method 2: Deploy via Railway CLI

1. **Install Railway CLI**:
   ```bash
   npm i -g @railway/cli
   # or
   brew install railway
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Initialize Project**:
   ```bash
   railway init
   ```

4. **Deploy**:
   ```bash
   railway up
   ```

5. **Generate Domain**:
   ```bash
   railway domain
   ```

### Setting Up Single Unified URL

To have both services under one domain (e.g., `app.yourdomain.com`):

#### Option A: Use Railway's Proxy (Simple)
Deploy frontend and configure it to proxy API requests:

1. Update `frontend/nginx.conf`:
```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Serve frontend
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Proxy API requests to backend
    location /api/ {
        proxy_pass http://backend:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

2. Update frontend to use `/api` instead of full URL:
```javascript
const API_BASE_URL = '/api';
```

#### Option B: Custom Domain (Professional)
1. Buy a domain (e.g., from Namecheap, Google Domains)
2. In Railway:
   - Frontend service → Settings → Custom Domain → Add `app.yourdomain.com`
   - Backend service → Settings → Custom Domain → Add `api.yourdomain.com`
3. Update DNS records as Railway instructs
4. Update frontend `REACT_APP_API_URL=https://api.yourdomain.com`

### Environment Variables

Set these in Railway dashboard for each service:

**Backend Service**:
```
PYTHONUNBUFFERED=1
```

**Frontend Service**:
```
REACT_APP_API_URL=https://your-backend-url.up.railway.app
```

### Monitoring & Logs

View logs in Railway dashboard:
- Click on service → Deployments → View Logs
- Monitor memory and CPU usage
- Set up alerts for errors

### Pricing

Railway pricing (as of 2026):
- **Hobby Plan**: $5/month credit (good for testing)
- **Developer Plan**: $20/month (recommended for production)
- Pay only for resources used (RAM, CPU, bandwidth)

Estimated costs for this app:
- Backend: ~$8-12/month (due to model size)
- Frontend: ~$2-3/month
- **Total**: ~$10-15/month

### Troubleshooting

**Issue**: Out of memory
- **Solution**: Increase memory in Railway settings (Service → Settings → Memory)

**Issue**: Frontend can't reach backend
- **Solution**: Check CORS settings in `main.py` and `REACT_APP_API_URL` in frontend

**Issue**: Slow cold starts
- **Solution**: Railway keeps services warm on paid plans

### Alternative: Render.com (Free Option)

If you want a completely free option:

1. Go to https://render.com
2. Create account and connect GitHub
3. Create two Web Services:
   - **Backend**: 
     - Docker
     - Free tier
     - Add environment variables
   - **Frontend**:
     - Docker
     - Free tier
     - Set `REACT_APP_API_URL` to backend URL

**Note**: Free tier on Render spins down after 15 minutes of inactivity (cold starts ~30 seconds)

### Best Practice: Use Railway for Production

For a production app with no cold starts and better performance:
1. Use Railway (or Fly.io)
2. Set up custom domain
3. Enable auto-scaling
4. Set up monitoring and alerts
5. Regular backups of your model file

---

## Quick Commands Reference

```bash
# Railway CLI
railway login                 # Login to Railway
railway init                  # Initialize project
railway up                    # Deploy
railway logs                  # View logs
railway domain                # Generate domain
railway open                  # Open in browser
railway run <command>         # Run command in Railway environment

# Local testing before deploy
docker-compose up --build     # Test locally
docker-compose logs -f        # View logs
docker-compose down           # Stop services
```

## Next Steps

1. Choose deployment platform (Railway recommended)
2. Push code to GitHub
3. Deploy using one of the methods above
4. Configure environment variables
5. Test the deployed application
6. (Optional) Set up custom domain

Your app will be live with a single URL! 🚀
