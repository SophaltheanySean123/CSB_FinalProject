from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from routes import health, quiz, analytics

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not found in the env")

app = FastAPI(
    title="AI Generated QUIZ",
    version="1.0.0.0",
    description="Generated Quiz from PDF or DOCX file using GEMINI AI"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=["*"]
)

app.include_router(health.router, tags=["health"])
app.include_router(quiz.router, tags=["Quiz"])
app.include_router(analytics.router, tags=["Analytics"])

@app.get("/")
async def root():
    "API INFORMATION"
    return{
        "service": "AI GENERATED QUIZ",
        "version" : "1.0.0",
        "status" : "online",
        "endpoint" : {
            "GET /heath" : "Check endpoint health",
            "POST /Quiz" : "Generate Quiz from PDF/DOCX files",
            "GET /docs" : "API documentation"              
            ""
         }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)