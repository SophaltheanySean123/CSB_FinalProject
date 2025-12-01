from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from routes.health import router as health_router
from routes.quiz import router as quiz_router
from routes.analytics import router as analytics_router

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not found in the env")

app = FastAPI(
    title="AI Generated QUIZ",
    version="1.0.0",
    description="Generated Quiz from PDF or DOCX file using GEMINI AI",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health_router, tags=["Health"])
app.include_router(quiz_router, tags=["Quiz"])
app.include_router(analytics_router, tags=["Analytics"])


@app.get("/")
async def root():
    return {
        "service": "AI GENERATED QUIZ - FastAPI",
        "version": "1.0.0",
        "status": "online",
        "framework": "FastAPI",
        "data_structures": {
            "hash_map": "QuestionCache - O(1) storage/retrieval",
            "queue": "QuizQueue (deque) - O(1) FIFO operations",
            "stack": "QuizHistory (list) - O(1) LIFO operations",
            "set": "used_questions - O(1) lookup"
        },
        "endpoints": {
            "POST /api/quiz/upload": "Upload and cache questions (Hash Map)",
            "POST /api/quiz/generate": "Generate quiz (Queue + Set)",
            "POST /api/quiz/submit": "Submit quiz results (Stack)",
            "GET /api/quiz/stats/{session_id}": "Get session statistics",
            "POST /api/quiz/reset": "Reset question pool",
            "GET /api/quiz/check-cache/{session_id}": "Check cache status"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
