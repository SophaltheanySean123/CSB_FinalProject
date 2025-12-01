from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables FIRST
load_dotenv()

# Check for API key
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not found in the .env file")

# Import routers AFTER loading env
from routes import health, quiz, analytics

# Create FastAPI app
app = FastAPI(
    title="AI Generated QUIZ",
    version="1.0.0",
    description="Generated Quiz from PDF or DOCX file using GEMINI AI"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(quiz.router, tags=["Quiz"])
app.include_router(analytics.router, tags=["Analytics"])

@app.get("/")
async def root():
    """API INFORMATION"""
    return {
        "service": "AI GENERATED QUIZ",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "GET /health": "Check endpoint health",
            "POST /quiz": "Generate Quiz from PDF/DOCX files",
            "GET /analytics/session/{session_id}": "Get quiz analytics",
            "GET /docs": "API documentation (Swagger UI)",
            "GET /redoc": "API documentation (ReDoc)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
