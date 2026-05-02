# AgriSen - Vercel Deployment Guide

## 📋 Prerequisites

Before deploying to Vercel, ensure you have:
- A Vercel account (free or paid)
- A GitHub repository with your code
- MongoDB Atlas account (free tier available)
- Redis cloud account (optional but recommended)
- OpenAI API key (optional for chatbot)
- Weather API key (OpenWeatherMap)
- Google OAuth credentials

## 📦 Step-by-Step Deployment

### Step 1: Prepare Your Environment Variables

1. Copy the `.env.example` file to understand all required variables
2. Create a `.env.local` file for local development (DO NOT commit this)
3. Note down all required environment variables:

```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/agrisen
REDIS_URL=redis://username:password@host:port
JWT_SECRET=your_secret_key
OPENAI_API_KEY=your_api_key
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_secret
WEATHER_API_KEY=your_api_key
VITE_API_URL=https://your-api-domain.com
VITE_GOOGLE_CLIENT_ID=your_client_id
```

### Step 2: Push Code to GitHub

```bash
git init
git add .
git commit -m "Initial commit: AgriSen crop recommendation system"
git branch -M main
git remote add origin https://github.com/yourusername/agrisen.git
git push -u origin main
```

### Step 3: Deploy Frontend on Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Set project name to "agrisen-frontend"
5. In "Framework Preset", select "Vite"
6. Root Directory: `frontend`
7. Build Command: `npm run build`
8. Output Directory: `dist`

**Environment Variables:**
Add the following in Vercel dashboard:
- `VITE_API_URL`: Your backend API URL
- `VITE_GOOGLE_CLIENT_ID`: Your Google OAuth ID

9. Click "Deploy"

### Step 4: Deploy Backend API on Vercel

**Important:** Vercel has limitations for Python backends in free tier. 

#### Option A: Using Vercel with Python Support (Recommended)

1. Create a new Vercel project for backend
2. In Root Directory: (leave as /)
3. Framework: Other (Python)
4. Build Command: `pip install -r backend/requirements.txt`
5. Install Command: `pip install -r backend/requirements.txt`

**Environment Variables in Vercel:**
```
MONGODB_URI=mongodb+srv://...
REDIS_URL=redis://...
JWT_SECRET=your_secret
OPENAI_API_KEY=your_api
GOOGLE_CLIENT_ID=your_id
GOOGLE_CLIENT_SECRET=your_secret
WEATHER_API_KEY=your_key
ENVIRONMENT=production
```

6. Configure `vercel.json` (already included)

#### Option B: Use an Alternative Backend Service (Recommended for Reliability)

For better performance and reliability, consider:

**Railway.app** (Recommended):
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Link to Vercel
railway link

# Deploy
railway up
```

**Render.com**:
1. Connect GitHub repo
2. Create new Web Service
3. Runtime: Python 3.11
4. Build Command: `pip install -r backend/requirements.txt`
5. Start Command: `uvicorn main:app --host 0.0.0.0 --port 8000`
6. Add all environment variables
7. Deploy

**PythonAnywhere or AWS Lambda**:
Follow their respective documentation.

### Step 5: Update Frontend API URL

After backend deployment, update frontend environment variable:

In Vercel Frontend Dashboard:
1. Go to Settings > Environment Variables
2. Update `VITE_API_URL` to your backend API URL (e.g., `https://api.yourdomain.com`)
3. Trigger a rebuild

### Step 6: Configure CORS in Backend

Edit `api/index.py` to update allowed origins:

```python
allowed_origins = [
    "https://your-frontend-vercel-url.vercel.app",
    "https://yourdomain.com",
]
```

### Step 7: Test the Deployment

1. Frontend: Visit https://your-frontend.vercel.app
2. Backend Health Check: https://your-api.vercel.app/health
3. API Docs: https://your-api.vercel.app/docs

## 🗄️ Database Configuration

### MongoDB Atlas Setup:

1. Go to [mongodb.com/cloud/atlas](https://mongodb.com/cloud/atlas)
2. Create a free cluster
3. Create database user with strong password
4. Whitelist all IPs (0.0.0.0/0)
5. Get connection string
6. Update `MONGODB_URI` in environment variables

### Redis Cloud Setup:

1. Go to [redis.com/cloud](https://redis.com/cloud)
2. Create free database
3. Get connection URL
4. Update `REDIS_URL` in environment variables

## 🔐 Security Best Practices

1. **Never commit `.env` files** - Use Vercel secrets
2. **Use strong JWT secrets** - Generate with: `openssl rand -hex 32`
3. **Enable MongoDB IP whitelisting**
4. **Use HTTPS only** - Vercel handles this
5. **Set secure CORS origins** - Only allow your domains
6. **Rotate API keys regularly**
7. **Use environment-specific secrets**

## 📊 Monitoring & Logs

### Vercel Logs:
1. Dashboard > Project > Settings > Logs
2. View build and runtime logs
3. Check deployment status

### Backend Logs (if using Railway/Render):
1. Check service dashboard
2. View application logs
3. Monitor resource usage

## 🚀 Production Optimization

### Frontend:
- ✅ Code splitting enabled in vite.config.js
- ✅ Asset optimization
- ✅ Gzip compression
- ✅ Image optimization

### Backend:
- Configure Redis caching
- Use database indexing
- Implement rate limiting
- Monitor API performance

## 🔄 Continuous Deployment

Both frontend and backend will auto-deploy on:
- Push to main branch
- Successful tests pass
- Environment variables updated

## ❌ Troubleshooting

### Frontend Won't Load:
- Check browser console for CORS errors
- Verify `VITE_API_URL` is correct
- Clear browser cache

### API 502/504 Errors:
- Check backend health endpoint
- Verify environment variables are set
- Check database connectivity
- Review backend logs

### CORS Errors:
- Update allowed origins in `api/index.py`
- Ensure API URL is in frontend config
- Clear backend cache/restart

### Database Connection Issues:
- Verify MongoDB URI format
- Check IP whitelist
- Test connection locally
- Verify credentials

## 📱 Custom Domain Setup

### Add Custom Domain on Vercel:

1. Frontend Dashboard > Settings > Domains
2. Add your domain (e.g., app.yourdomain.com)
3. Update DNS records at domain registrar:
   - Type: CNAME
   - Name: app
   - Value: cname.vercel-dns.com

## 📞 Support & Resources

- Vercel Docs: https://vercel.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- MongoDB Docs: https://docs.mongodb.com
- React Docs: https://react.dev

## ✅ Deployment Checklist

- [ ] Environment variables configured
- [ ] MongoDB Atlas cluster created and URI set
- [ ] Redis URL configured (optional)
- [ ] Google OAuth credentials set
- [ ] API keys obtained (Weather, OpenAI)
- [ ] CORS origins configured
- [ ] Frontend deployed on Vercel
- [ ] Backend deployed (Railway/Render/Vercel)
- [ ] Frontend API URL updated
- [ ] Health endpoints responding
- [ ] Database migrations complete
- [ ] Logs being monitored
- [ ] Custom domain configured (optional)
- [ ] SSL certificate valid
- [ ] Performance optimized

## 🎯 Next Steps

1. Monitor application performance
2. Set up error tracking (Sentry)
3. Configure automated backups
4. Implement analytics
5. Plan for scaling

---

**Happy Deploying! 🚀**
