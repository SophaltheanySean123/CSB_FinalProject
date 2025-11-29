from pydantic import BaseModel
from typing import Optional

class QuizQuestion(BaseModel):
    """Schema for a single quiz question"""
    question: str
    options: dict
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    """Schema for quiz generation response"""
    success: bool
    questions: list[QuizQuestion]
    total_questions: int
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    success: bool
    error: str
    details: Optional[str] = None