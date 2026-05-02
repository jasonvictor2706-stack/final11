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
