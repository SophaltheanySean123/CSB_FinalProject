from fastapi import APIRouter, UploadFile, HTTPException, File, Form, Request
import os
from models.model import QuizResponse
from services.file_handler import extract_text_from_file
from services.quiz_generator import generate_quiz_with_retry
from utils.helpers import parse_JSON_quiz, validate_quiz
from utils.quiz_manager import quiz_manager

router = APIRouter()

# ============================================================
# Generate Quiz from PDF / DOCX / TXT
# ============================================================
@router.post("/generate_quiz", response_model=QuizResponse)
async def generate_quiz(
    file: UploadFile = File(...),
    num_of_questions: int = Form(default=10, ge=1, le=40)
):
    if not (
        file.filename.endswith(".pdf") 
        or file.filename.endswith(".docx") 
        or file.filename.endswith(".txt")
    ):
        raise HTTPException(400, "Only PDF, DOCX, and TXT files are supported")

    temp_path = None

    try:
        os.makedirs("temp", exist_ok=True)
        temp_path = f"temp/{file.filename}"

        # Save uploaded file temporarily
        with open(temp_path, "wb") as f:
            content = await file.read()
            if not content:
                raise HTTPException(400, "Empty file")
            f.write(content)

        # Extract text
        lesson_content = extract_text_from_file(temp_path, file.filename)
        if not lesson_content or len(lesson_content.strip()) < 100:
            raise HTTPException(400, "Could not extract sufficient text from file")

        # Generate quiz with AI
        result = generate_quiz_with_retry(lesson_content, num_of_questions)
        if not result.get("success"):
            raise HTTPException(503, result.get("message", "Failed to generate quiz"))

        # Save raw Gemini response to JSON file
        import json
        from datetime import datetime
        os.makedirs("gemini_responses", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        response_file = f"gemini_responses/gemini_response_{timestamp}.json"
        with open(response_file, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": timestamp,
                "raw_response": result["text"],
                "num_questions": num_of_questions,
                "file_name": file.filename
            }, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved Gemini response to: {response_file}")

        # Parse & validate JSON
        quiz_data = parse_JSON_quiz(result["text"])
        if not quiz_data:
            raise HTTPException(500, "Failed to parse quiz JSON")

        is_valid, validation_msg = validate_quiz(quiz_data)
        if not is_valid:
            raise HTTPException(500, f"Invalid quiz format: {validation_msg}")

        return {
            "success": True,
            "questions": quiz_data["questions"],
            "total_questions": len(quiz_data["questions"]),
            "message": f"Successfully generated {len(quiz_data['questions'])} questions"
        }

    except Exception as e:
        raise HTTPException(500, f"Internal error: {str(e)}")

    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass


# ============================================================
# Upload & Cache Questions (Hash Map)
# ============================================================
@router.post("/api/quiz/upload")
async def upload_questions(request: Request):
    try:
        data = await request.json()
        session_id = data.get("sessionId")
        questions = data.get("questions", [])
        metadata = data.get("metadata", {})

        if not session_id or not questions:
            return {"success": False, "error": "Session ID + questions required"}

        result = quiz_manager.upload_and_cache_questions(
            session_id=session_id, questions=questions, metadata=metadata
        )

        return result
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================
# Generate Quiz from Cached Questions (Queue + Set)
# ============================================================
@router.post("/api/quiz/generate")
async def generate_quiz_from_cache(request: Request):
    try:
        data = await request.json()
        session_id = data.get("sessionId")
        num_questions = data.get("numQuestions", 10)
        allow_repeats = data.get("allowRepeats", False)

        if not session_id:
            return {"success": False, "error": "Session ID is required"}

        result = quiz_manager.generate_new_quiz(
            session_id=session_id,
            num_questions=num_questions,
            allow_repeats=allow_repeats,
        )

        return result
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================
# Submit Completed Quiz (Stack – History)
# ============================================================
@router.post("/api/quiz/submit")
async def submit_quiz(request: Request):
    try:
        data = await request.json()
        session_id = data.get("sessionId")

        quiz_data = {
            "questions": data.get("questions", []),
            "score": data.get("score", 0),
            "total": data.get("total", 0),
            "start_time": data.get("start_time"),
            "end_time": data.get("end_time"),
            "total_time": data.get("total_time"),
            "per_question_time": data.get("per_question_time", []),
        }

        if not session_id:
            return {"success": False, "error": "Session ID is required"}

        return quiz_manager.submit_quiz_results(session_id, quiz_data)

    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================
# Session Statistics
# ============================================================
@router.get("/api/quiz/stats/{session_id}")
async def get_session_stats(session_id: str):
    try:
        return quiz_manager.get_session_stats(session_id)
    except Exception as e:
        raise HTTPException(500, str(e))


# ============================================================
# Reset Session (Clear Queue + Stack + Sets)
# ============================================================
@router.post("/api/quiz/reset")
async def reset_session(request: Request):
    try:
        data = await request.json()
        session_id = data.get("sessionId")
        keep_cache = data.get("keepCache", True)

        if not session_id:
            raise HTTPException(400, "Session ID is required")

        return quiz_manager.reset_session(session_id, keep_cache)
    except Exception as e:
        raise HTTPException(500, str(e))


# ============================================================
# Check Cached Questions
# ============================================================
@router.get("/api/quiz/check-cache/{session_id}")
async def check_cache(session_id: str):
    try:
        has_cache = quiz_manager.question_cache.has_questions(session_id)

        if has_cache:
            return {
                "has_cache": True,
                "total_questions": len(quiz_manager.question_cache.get_questions(session_id)),
                "metadata": quiz_manager.question_cache.get_metadata(session_id),
            }
        
        return {"has_cache": False, "message": "No cached questions"}

    except Exception as e:
        raise HTTPException(500, str(e))
