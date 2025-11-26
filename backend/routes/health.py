from fastapi import APIRouter
from fastapi.responses import JSONResponse
from google import genai

import os
from dotenv import load_dotenv

router = APIRouter()
load_dotenv()  # Load environment variables

# Get API key
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

@router.get("/health")
async def health():
    try:
        test_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Say OK"
        )
        return {
            "status" :"healthy",
            "gemini-ai" : "connected",
            "messages" : "All systems are operating"
        }

    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "gemini_api": "disconnected",
                "error": str(e)
            }
        )

