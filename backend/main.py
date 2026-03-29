from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
try:
    from .routes import router
except ImportError:
    from routes import router


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

# Include routes
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
