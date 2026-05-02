"""
FastAPI App (NOT for Vercel serverless)
This will be used later on Render/Railway
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

# Import routes
from database.connection import connect_db, close_db
from routes import auth, predict, weather, fertilizer, chatbot


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title="AgriSen API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

if os.getenv("ENVIRONMENT") == "production":
    allowed_origins.append("*")  # allow all in production (simplify for now)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(weather.router, prefix="/weather")
app.include_router(fertilizer.router, prefix="/api")
app.include_router(chatbot.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "AgriSen API running"}


@app.get("/health")
async def health():
    return {"status": "ok"}
