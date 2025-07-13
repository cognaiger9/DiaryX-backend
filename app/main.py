from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.api_v1.api import api_router

app = FastAPI(
    title="DiaryX API",
    description="API for tracking time spent on side projects",
    version="1.0.0"
)

# Configure CORS for Railway deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://*.railway.app",  # Railway domains
        "https://*.up.railway.app",  # Railway domains
        "*"  # Allow all origins for development (restrict in production)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to DiaryX API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 