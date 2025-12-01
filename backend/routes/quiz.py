from fastapi import APIRouter, UploadFile, HTTPException, File, Form, Request
import os
from models.model import QuizResponse
from services.file_handler import extract_text_from_file
from services.quiz_generator import generate_quiz_with_retry
from utils.helpers import parse_JSON_quiz, validate_quiz
from utils.quiz_manager import quiz_manager

router = APIRouter()
@router.post("/generate_quiz", response_model=QuizResponse)
async def generate_quiz(
        file: UploadFile = File(...),
        num_of_questions: int = Form(default=10, ge=1, le=40, description="Number of questions to generate (1-40)")):

    if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx") or file.filename.endswith(".txt")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF, DOCS, and TXT files are supported"
        )
    temp_path = None

    try:
        os.makedirs("temp", exist_ok=True)
        temp_path = f"temp/{file.filename}"

        with open(temp_path, "wb") as f:
            content = await file.read()
            if len(content) == 0:
                raise HTTPException(status_code=400, detail="Empty file")
            f.write(content)

        lesson_content = extract_text_from_file(temp_path, file.filename)

        if not lesson_content or len(lesson_content.strip()) < 100:
            raise HTTPException(
                status_code=400,
                detail="Could not extract sufficient text from file"
            )

            # Generate quiz using AI
        result = generate_quiz_with_retry(lesson_content, num_of_questions)

        if not result.get("success"):
            error_message = result.get("message", "Failed to generate quiz")
            print(f"Quiz generation failed: {error_message}")
            print(f"Full result: {result}")
            raise HTTPException(
                status_code=503,
                detail=error_message
            )
        # Parse JSON response
        quiz_data = parse_JSON_quiz(result["text"])

        if not quiz_data:
            raise HTTPException(
                status_code=500,
                detail="Failed to parse quiz response from AI"
            )
        # Validate quiz structure
        is_valid, validation_msg = validate_quiz(quiz_data)

        if not is_valid:
            raise HTTPException(
                status_code=500,
                detail=f"Invalid quiz format: {validation_msg}"
            )
        # Return successful response
        return {
            "success": True,
            "questions": quiz_data["questions"],
            "total_questions": len(quiz_data["questions"]),
            "message": f"Successfully generated {len(quiz_data['questions'])} questions"
        }

    except HTTPException:
        raise

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        import traceback
        error_detail = f"Internal server error: {str(e)}"
        print(f"Error details: {error_detail}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=error_detail
        )

    finally:
    # Cleanup: Delete temporary file
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass


@router.post('/api/quiz/upload')
async def upload_questions(request: Request):
    """
    Upload and cache questions from file (FastAPI)
    Uses Hash Map for O(1) storage
    """
    try:
        data = await request.json()
        session_id = data.get('sessionId')
        questions = data.get('questions', [])
        metadata = data.get('metadata', {})

        if not session_id or not questions:
            return { 'success': False, 'error': 'Session ID and questions are required' }

        result = quiz_manager.upload_and_cache_questions(
            session_id=session_id,
            questions=questions,
            metadata=metadata
        )

        return result

    except Exception as e:
        return { 'success': False, 'error': str(e) }


@router.post('/api/quiz/generate')
async def generate_quiz_from_cache(request: Request):
    """
    Generate new quiz from cached questions without re-uploading
    Uses Queue for FIFO distribution and Set for O(1) duplicate checking
    """
    try:
        data = await request.json()
        session_id = data.get('sessionId')
        num_questions = data.get('numQuestions', 10)
        allow_repeats = data.get('allowRepeats', False)

        if not session_id:
            return { 'success': False, 'error': 'Session ID is required' }

        result = quiz_manager.generate_new_quiz(
            session_id=session_id,
            num_questions=num_questions,
            allow_repeats=allow_repeats
        )

        if not result.get('success'):
            return result

        return result

    except Exception as e:
        return { 'success': False, 'error': str(e) }


@router.post('/api/quiz/submit')
async def submit_quiz(request: Request):
    """
    Submit completed quiz results to Stack (history)
    """
    try:
        data = await request.json()
        session_id = data.get('sessionId')
        # Accept timing fields if provided
        quiz_data = {
            'questions': data.get('questions', []),
            'score': data.get('score', 0),
            'total': data.get('total', 0),
            'start_time': data.get('start_time'),
            'end_time': data.get('end_time'),
            'total_time': data.get('total_time'),
            'per_question_time': data.get('per_question_time', [])
        }

        if not session_id:
            return { 'success': False, 'error': 'Session ID is required' }

        result = quiz_manager.submit_quiz_results(session_id, quiz_data)

        return result

    except Exception as e:
        return { 'success': False, 'error': str(e) }


@router.get('/api/quiz/stats/{session_id}')
async def get_session_stats(session_id: str):
    """
    Get session statistics from all data structures
    """
    try:
        stats = quiz_manager.get_session_stats(session_id)
        return stats

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/api/quiz/reset')
async def reset_session(request: Request):
    """
    Reset session question pool
    """
    try:
        data = await request.json()
        session_id = data.get('sessionId')
        keep_cache = data.get('keepCache', True)
        
        if not session_id:
            raise HTTPException(status_code=400, detail='Session ID is required')
        
        result = quiz_manager.reset_session(session_id, keep_cache)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/api/quiz/check-cache/{session_id}')
async def check_cache(session_id: str):
    """
    Check if session has cached questions
    """
    try:
        has_cache = quiz_manager.question_cache.has_questions(session_id)
        
        if has_cache:
            questions = quiz_manager.question_cache.get_questions(session_id)
            metadata = quiz_manager.question_cache.get_metadata(session_id)
            
            return { 'has_cache': True, 'total_questions': len(questions), 'metadata': metadata }
        else:
            return { 'has_cache': False, 'message': 'No cached questions found' }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
