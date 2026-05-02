# 🚀 AgriSen - Setup & Deployment Instructions

## ✅ Project Overview

AgriSen is a full-stack web application for explainable AI-based crop recommendation. It consists of:
- **Frontend**: React + Vite (deployed on Vercel)
- **Backend**: FastAPI + Python (deployed on Railway/Render or Vercel)
- **Database**: MongoDB Atlas (cloud)
- **Cache**: Redis (optional)

## 📋 What's Changed for Vercel Deployment

### New Files Created:
1. **`vercel.json`** - Vercel configuration
2. **`.env.example`** - Environment variables template
3. **`api/index.py`** - Serverless API handler
4. **`DEPLOYMENT_GUIDE.md`** - Complete deployment guide
5. **Updated `package.json`** - Build scripts added
6. **Updated `backend/requirements.txt`** - Production dependencies

### Updated Files:
- **`backend/main.py`** → **`backend/main.py.updated`**
  - Added environment variable support
  - Updated CORS configuration for production
  - Added health check endpoint

- **`frontend/vite.config.js`** → **`frontend/vite.config.updated.js`**
  - Added code splitting optimization
  - Added build optimization
  - Added proxy configuration for development

## 🔧 Local Setup (Before Deployment)

### 1. Install Dependencies

```bash
# Install all dependencies
npm run install:all

# Or manually:
npm install
cd frontend && npm install
cd ../backend && pip install -r requirements.txt
```

### 2. Setup Environment Variables

```bash
# Copy the example file
cp .env.example .env.local

# Edit with your values
nano .env.local
```

Required variables:
```
MONGODB_URI=your_mongodb_connection_string
REDIS_URL=your_redis_url (optional)
JWT_SECRET=generate_with_openssl_rand_-hex_32
OPENAI_API_KEY=your_openai_key
GOOGLE_CLIENT_ID=your_google_oauth_id
GOOGLE_CLIENT_SECRET=your_google_secret
WEATHER_API_KEY=your_weather_api_key
VITE_API_URL=http://localhost:8000
VITE_GOOGLE_CLIENT_ID=your_google_oauth_id
```

### 3. Create `.env.local` for Backend

Create `backend/.env.local` with the same variables.

### 4. Run Locally

```bash
# Run both frontend and backend together
npm run dev

# Or separately:
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

The app should be available at:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📦 Deployment Steps

### Step 1: Update Files

Replace original files with updated versions:

```bash
# Backend main.py
cp backend/main.py backend/main.py.backup
cp backend/main.py.updated backend/main.py

# Frontend vite config
cp frontend/vite.config.js frontend/vite.config.js.backup
cp frontend/vite.config.updated.js frontend/vite.config.js
```

### Step 2: Push to GitHub

```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### Step 3: Frontend Deployment on Vercel

1. Go to https://vercel.com
2. Click "Add New..." → "Project"
3. Import your GitHub repo
4. Set these settings:
   - **Project Name**: agrisen-frontend
   - **Framework Preset**: Vite
   - **Root Directory**: frontend
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

5. Add Environment Variables:
   ```
   VITE_API_URL=https://your-backend-url.com
   VITE_GOOGLE_CLIENT_ID=your_google_id
   ```

6. Click Deploy ✅

### Step 4: Backend Deployment (Choose ONE option)

#### Option A: Railway.app (Recommended - Easy Python Support)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize Railway project
railway init

# Set environment variables
railway variables set MONGODB_URI=mongodb+srv://...
railway variables set JWT_SECRET=your_secret
# ... (add all other variables)

# Deploy
railway up
```

#### Option B: Render.com

1. Go to https://render.com
2. Create New Web Service
3. Connect GitHub repo
4. Set:
   - **Name**: agrisen-api
   - **Environment**: Python 3.11
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 8000`
5. Add all environment variables
6. Deploy

#### Option C: Vercel Python Support

1. Create new Vercel project from same repo
2. Root Directory: `/`
3. Runtime: Python
4. Add environment variables
5. Configure `vercel.json` (already provided)

### Step 5: Update Frontend with Backend URL

After backend is deployed:

1. Go to Vercel Frontend Dashboard
2. Settings → Environment Variables
3. Update `VITE_API_URL` to your backend URL (e.g., https://api.yourdomain.com)
4. Redeploy frontend

## 🎯 Deployment Checklist

```
BEFORE DEPLOYING:
☐ All .env variables are prepared
☐ MongoDB Atlas account created
☐ Google OAuth credentials obtained
☐ API keys obtained (Weather, OpenAI, etc.)
☐ Files updated (main.py, vite.config.js)
☐ Code pushed to GitHub

FRONTEND DEPLOYMENT:
☐ Vercel project created and linked
☐ Build settings configured correctly
☐ Environment variables set
☐ Frontend deployed successfully
☐ URL noted (e.g., https://agrisen-frontend.vercel.app)

BACKEND DEPLOYMENT:
☐ Backend service created (Railway/Render/Vercel)
☐ Python environment configured
☐ All environment variables set
☐ Start command configured
☐ Build successful
☐ API responding (/health endpoint)
☐ API URL noted (e.g., https://agrisen-api.railway.app)

POST DEPLOYMENT:
☐ Frontend VITE_API_URL updated with backend URL
☐ Frontend redeployed
☐ CORS origins updated in backend
☐ Backend redeployed
☐ Test health check: https://your-api/health
☐ Test frontend loads: https://your-frontend.vercel.app
☐ Test login/registration works
☐ Logs being monitored
```

## 🔍 Testing After Deployment

### Frontend Tests:
1. Visit your Vercel frontend URL
2. Check browser console for errors
3. Test navigation between pages
4. Test if API calls work

### Backend Tests:
```bash
# Check health
curl https://your-api/health

# Check docs
https://your-api/docs

# Test a simple endpoint
curl -X GET https://your-api/regions
```

## ❌ Common Issues & Solutions

### Issue: CORS Errors
```
Blocked by CORS policy
```
**Solution**: Update `allowed_origins` in `backend/main.py` with your frontend URL

### Issue: 404 on Frontend Routes
**Solution**: Ensure Vercel rewrites are configured correctly (handled in `vercel.json`)

### Issue: Database Connection Failed
**Solution**: 
- Verify MongoDB URI format
- Check IP whitelist in MongoDB Atlas (allow 0.0.0.0/0 for Vercel)
- Test connection locally first

### Issue: API 502/504 Errors
**Solution**:
- Check backend logs
- Verify all environment variables are set
- Restart backend service
- Check if backend is actually running

### Issue: Build Fails
**Solution**:
- Check build logs in Vercel dashboard
- Verify Node version compatibility
- Ensure all dependencies are installed
- Test build locally: `npm run build:all`

## 📊 Performance Optimization

### Frontend:
- Code is automatically split in Vite build
- Images optimized automatically
- Gzip compression enabled by default

### Backend:
- Add Redis caching for frequently accessed data
- Use database indexing for common queries
- Implement rate limiting on public endpoints

## 🔐 Security Reminders

1. ✅ Never commit `.env` files
2. ✅ Use strong, unique JWT secrets
3. ✅ Keep API keys private
4. ✅ Use HTTPS only (Vercel handles this)
5. ✅ Whitelist only necessary CORS origins
6. ✅ Update dependencies regularly

## 📚 Resources

- **Vercel Docs**: https://vercel.com/docs
- **FastAPI**: https://fastapi.tiangolo.com
- **React**: https://react.dev
- **MongoDB**: https://docs.mongodb.com
- **Railway**: https://docs.railway.app
- **Render**: https://render.com/docs

## 🆘 Need Help?

1. Check `DEPLOYMENT_GUIDE.md` for detailed steps
2. Review backend logs
3. Check Vercel/Railway/Render dashboards
4. Test locally first
5. Read service documentation

---

**You're all set! Happy deploying! 🚀**
