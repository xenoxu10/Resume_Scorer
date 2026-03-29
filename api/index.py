"""
Vercel serverless function entry point for FastAPI application
"""
import os
import sys
from pathlib import Path

# Add backend directory to path for imports
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Import routes from backend
try:
    from routes import router
except ImportError:
    from backend.routes import router

# Create FastAPI app
app = FastAPI(
    title="RAG Resume Scorer",
    description="Resume scoring system using RAG and OpenAI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api", tags=["Resume Analysis"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "RAG Resume Scorer API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "analyze": "/api/analyze (POST with files)",
            "analyze-text": "/api/analyze-text (POST with text)",
            "health": "/api/health (GET)"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": os.getenv("ENVIRONMENT", "development")
    }


# Mount frontend static files if available
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="frontend")


# Serve index.html for SPA routing
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """Serve SPA index.html for any unmatched routes"""
    frontend_index = Path(__file__).parent.parent / "frontend" / "index.html"
    if frontend_index.exists():
        return FileResponse(str(frontend_index))
    return {"error": "Frontend not found"}
