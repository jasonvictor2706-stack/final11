# 📝 Complete Code Changes for Vercel Deployment

## Summary of Changes

This document contains all the code changes, new files, and configurations needed to deploy AgriSen on Vercel.

---

## 1️⃣ NEW FILE: `vercel.json`

**Purpose**: Configuration file for Vercel deployment

```json
{
  "buildCommand": "npm run build:all",
  "outputDirectory": "frontend/dist",
  "rewrites": [
    {
      "source": "/api/v1/(.*)",
      "destination": "/api/v1/$1"
    },
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ],
  "env": {
    "MONGODB_URI": "@mongodb_uri",
    "REDIS_URL": "@redis_url",
    "JWT_SECRET": "@jwt_secret",
    "OPENAI_API_KEY": "@openai_api_key",
    "GOOGLE_CLIENT_ID": "@google_client_id",
    "GOOGLE_CLIENT_SECRET": "@google_client_secret",
    "WEATHER_API_KEY": "@weather_api_key"
  },
  "functions": {
    "api/v1/[...].py": {
      "runtime": "python3.11"
    }
  }
}
```

**Location**: Root directory of project

---

## 2️⃣ NEW FILE: `.env.example`

**Purpose**: Template for environment variables

```env
# MongoDB Configuration
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/agrisen

# Redis Configuration
REDIS_URL=redis://username:password@host:port/db

# JWT Authentication
JWT_SECRET=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Email Configuration (Gmail or SendGrid)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=https://yourdomain.com/auth/google/callback

# Weather API
WEATHER_API_KEY=your_openweathermap_api_key

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Frontend Configuration
VITE_API_URL=https://api.yourdomain.com
VITE_GOOGLE_CLIENT_ID=your_google_client_id

# Environment
ENVIRONMENT=production
DEBUG=False
```

**Location**: Root directory of project

---

## 3️⃣ NEW FILE: `api/index.py`

**Purpose**: Serverless handler for Vercel Python functions

```python
"""
Vercel Serverless Function Handler for FastAPI Backend
This file allows Vercel to run the FastAPI application as serverless functions
"""

import sys
import os
from pathlib import Path

# Add backend directory to Python path
backend_path = Path(__file__).parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import routes from backend
from database.connection import connect_db, close_db
from routes import auth, predict, weather, fertilizer, chatbot


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title="AgriSen API",
    description="Explainable AI Framework for Intelligent Crop Recommendation",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Configuration for Vercel deployment
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

# Add production domain when deployed
if os.getenv("ENVIRONMENT") == "production":
    allowed_origins.extend([
        "https://yourdomain.vercel.app",
        "https://yourdomain.com",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(weather.router, prefix="/weather")
app.include_router(fertilizer.router, prefix="/api", tags=["Fertilizer"])
app.include_router(chatbot.router, prefix="/api")


@app.get("/")
async def root():
    return {
        "app": "AgriSen",
        "version": "1.0.0",
        "description": "Explainable AI Crop Recommendation API",
        "docs": "/api/docs",
        "health": "/api/health",
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
```

**Location**: `api/` directory (create this directory if it doesn't exist)

---

## 4️⃣ UPDATED FILE: `package.json` (Root)

**Changes**: Added build scripts for full-stack deployment

```json
{
    "name": "agrisen-root",
    "version": "1.0.0",
    "description": "Root folder for AgriSen - Explainable AI Crop Recommendation System",
    "scripts": {
        "install:all": "npm install && cd frontend && npm install",
        "dev": "concurrently \"cd backend && uvicorn main:app --reload\" \"cd frontend && npm run dev\"",
        "build:frontend": "cd frontend && npm run build",
        "build:all": "npm run build:frontend",
        "preview:frontend": "cd frontend && npm run preview",
        "start": "node server.js"
    },
    "devDependencies": {
        "concurrently": "^8.2.1"
    }
}
```

**Location**: Root directory (replace existing)

---

## 5️⃣ UPDATED FILE: `backend/requirements.txt`

**Changes**: Added production-ready dependencies with pinned versions

```
fastapi==0.110.0
uvicorn[standard]==0.29.0
pymongo==4.6.3
motor==3.4.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt<4.0.0
pandas==2.2.1
joblib==1.3.2
shap==0.45.0
scikit-learn==1.4.1.post1
python-dotenv==1.0.1
python-multipart==0.0.9
requests>=2.31.0
redis>=5.0.0
aioredis>=2.0.1
openai>=1.0.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
```

**Location**: `backend/requirements.txt` (replace existing)

---

## 6️⃣ UPDATED FILE: `backend/main.py`

**Changes**: Added environment variable support and Vercel compatibility

```python
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from database.connection import connect_db, close_db
from routes import auth, predict, weather, fertilizer, chatbot


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title="AgriSen API",
    description="Explainable AI Framework for Intelligent Crop Recommendation",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS Configuration ────────────────────────────────────────────────────────
# Development origins
dev_origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5175",
    "http://127.0.0.1:3000",
]

# Production origins - Update with your actual domains
prod_origins = [
    "https://yourdomain.vercel.app",  # Update with your frontend domain
    "https://yourdomain.com",          # Update with your custom domain
]

# Select origins based on environment
allowed_origins = dev_origins if os.getenv("ENVIRONMENT") != "production" else prod_origins + dev_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(weather.router, prefix="/weather")
app.include_router(fertilizer.router, prefix="/api", tags=["Fertilizer"])
app.include_router(chatbot.router, prefix="/api")


@app.get("/")
async def root():
    return {
        "app": "AgriSen",
        "version": "1.0.0",
        "description": "Explainable AI Crop Recommendation API",
        "docs": "/docs",
        "environment": os.getenv("ENVIRONMENT", "development"),
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "version": "1.0.0",
    }


# Export app for Vercel
__all__ = ["app"]
```

**Location**: `backend/main.py` (replace existing)

**What changed**:
- Added `import os` and `from dotenv import load_dotenv`
- Added `load_dotenv()` to load env variables
- Separated dev and prod CORS origins
- Made CORS origins configurable via environment
- Enhanced health check endpoint
- Added `__all__` export for Vercel

---

## 7️⃣ UPDATED FILE: `frontend/vite.config.js`

**Changes**: Added optimization and build configuration

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    minify: 'terser',
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor': ['react', 'react-dom', 'react-router-dom'],
          'ui': ['@heroicons/react', 'lucide-react'],
          'charts': ['recharts'],
        }
      }
    }
  },
  preview: {
    port: 3000
  }
})
```

**Location**: `frontend/vite.config.js` (replace existing)

**What changed**:
- Added development server proxy configuration
- Added build optimization options
- Added code splitting for better performance
- Added source maps for production debugging
- Added preview server configuration

---

## 📄 NEW DOCUMENTATION FILES

### 8️⃣ `DEPLOYMENT_GUIDE.md`
Complete step-by-step deployment guide with:
- Prerequisites checklist
- Frontend deployment instructions
- Backend deployment options (Railway, Render, Vercel)
- Database setup (MongoDB Atlas, Redis)
- Security best practices
- Troubleshooting guide

### 9️⃣ `SETUP_INSTRUCTIONS.md`
Quick setup and local development guide with:
- Project overview
- What's changed summary
- Local setup instructions
- Deployment checklist
- Common issues and solutions
- Performance optimization tips

### 🔟 `CHANGES_SUMMARY.md` (This file)
Complete list of all changes

---

## ✅ How to Apply These Changes

### Option 1: Manual Update (Safe - Review Each Change)

```bash
# 1. Create api directory
mkdir -p api

# 2. Add new files
touch vercel.json
touch .env.example
touch api/index.py
touch DEPLOYMENT_GUIDE.md
touch SETUP_INSTRUCTIONS.md

# 3. Update existing files using provided code above
# - Replace package.json (root)
# - Replace backend/requirements.txt
# - Replace backend/main.py
# - Replace frontend/vite.config.js

# 4. Test locally
npm run dev

# 5. Push to GitHub
git add .
git commit -m "Setup Vercel deployment configuration"
git push origin main
```

### Option 2: Copy Complete Modified Project

```bash
# Copy entire project from outputs
cp -r modified-agrisen-project/* ./
```

---

## 🔄 Migration Path

### From Current to Production:

1. **Local Testing**:
   - Apply all changes
   - Test with `npm run dev`
   - Verify API calls work

2. **GitHub Setup**:
   - Push to repository
   - Ensure `.env.local` is in `.gitignore`

3. **Frontend Deployment**:
   - Connect Vercel to GitHub
   - Set environment variables
   - Deploy

4. **Backend Deployment**:
   - Choose Railway, Render, or Vercel
   - Set all environment variables
   - Deploy

5. **Integration**:
   - Update frontend `VITE_API_URL`
   - Redeploy frontend
   - Test complete flow

---

## 🚨 Important Notes

### Before Pushing to GitHub:

```bash
# 1. Create .gitignore entries (if not present)
echo ".env.local" >> .gitignore
echo ".env" >> .gitignore
echo "backend/.env" >> .gitignore
echo "node_modules/" >> .gitignore
echo ".venv/" >> .gitignore
```

### Environment Variables Setup:

1. **Get all API keys** before deployment:
   - MongoDB Atlas connection string
   - Google OAuth credentials
   - OpenWeather API key
   - OpenAI API key (if using chatbot)
   - JWT Secret (generate: `openssl rand -hex 32`)

2. **Set in Vercel Dashboard**:
   - Frontend project: `VITE_API_URL`, `VITE_GOOGLE_CLIENT_ID`
   - Backend project: All variables listed in `.env.example`

### CORS Configuration:

Update both `api/index.py` and `backend/main.py`:
```python
prod_origins = [
    "https://YOUR_FRONTEND_DOMAIN.vercel.app",
    "https://your-custom-domain.com",
]
```

---

## 📊 File Structure After Changes

```
agrisen/
├── api/
│   └── index.py                 [NEW - Vercel handler]
├── backend/
│   ├── main.py                  [UPDATED]
│   ├── requirements.txt          [UPDATED]
│   ├── routes/
│   ├── services/
│   ├── database/
│   └── ...
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.js           [UPDATED]
│   └── ...
├── .env.example                 [NEW]
├── vercel.json                  [NEW]
├── package.json                 [UPDATED]
├── DEPLOYMENT_GUIDE.md          [NEW]
├── SETUP_INSTRUCTIONS.md        [NEW]
├── .gitignore
└── README.md
```

---

## ✨ What Each File Does

| File | Purpose | Created/Updated |
|------|---------|-----------------|
| `vercel.json` | Vercel deployment configuration | Created |
| `.env.example` | Environment variables template | Created |
| `api/index.py` | Serverless FastAPI handler | Created |
| `DEPLOYMENT_GUIDE.md` | Detailed deployment instructions | Created |
| `SETUP_INSTRUCTIONS.md` | Quick setup guide | Created |
| `package.json` | NPM build scripts | Updated |
| `backend/requirements.txt` | Python dependencies | Updated |
| `backend/main.py` | FastAPI app with env support | Updated |
| `frontend/vite.config.js` | Vite optimization config | Updated |

---

## 🎯 Next Steps

1. ✅ Review all changes above
2. ✅ Apply changes to your project
3. ✅ Create `.env.local` with your values
4. ✅ Test locally with `npm run dev`
5. ✅ Push to GitHub
6. ✅ Follow `DEPLOYMENT_GUIDE.md` for deployment
7. ✅ Monitor logs and test API endpoints

---

**Ready to deploy? Check out `DEPLOYMENT_GUIDE.md` for step-by-step instructions! 🚀**
