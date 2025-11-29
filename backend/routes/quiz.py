from fastapi import APIRouter, UploadFile, HTTPException, File, Form
import os
from models.model import QuizResponse
from services.file_handler import extract_text_from_file
from services.quiz_generator import generate_quiz_with_retry
from utils.helpers import parse_JSON_quiz, validate_quiz

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
