from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
from datetime import datetime
import numpy as np

# Change from Flask Blueprint to FastAPI Router
router = APIRouter()  # ← Changed from analytics_bp = Blueprint(...)

# Temporary in-memory storage for quiz results (session-based)
quiz_sessions = {}

# Pydantic models for request validation
class QuestionData(BaseModel):
    question: str
    userAnswer: str
    correctAnswer: str
    isCorrect: bool
    timeSpent: float

class QuizSubmission(BaseModel):
    sessionId: str
    topic: str
    questions: List[QuestionData]

# Change from @analytics_bp.route to @router.post
@router.post('/api/analytics/submit-quiz')
async def submit_quiz_results(submission: QuizSubmission):
    """
    Store quiz results and return analytics data
    """
    try:
        session_id = submission.sessionId
        
        # Store in session
        if session_id not in quiz_sessions:
            quiz_sessions[session_id] = []
        
        quiz_result = {
            'timestamp': datetime.now().isoformat(),
            'topic': submission.topic,
            'questions': [q.dict() for q in submission.questions]
        }
        
        quiz_sessions[session_id].append(quiz_result)
        
        return {
            'success': True,
            'message': 'Quiz results stored successfully'
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Change from @analytics_bp.route to @router.get
@router.get('/api/analytics/session/{session_id}')
async def get_session_analytics(session_id: str):
    """
    Get comprehensive analytics for a session using pandas
    """
    try:
        if session_id not in quiz_sessions or not quiz_sessions[session_id]:
            raise HTTPException(
                status_code=404,
                detail='No quiz data found for this session'
            )
        
        # Get all quizzes for this session
        session_quizzes = quiz_sessions[session_id]
        
        # Flatten all questions into a DataFrame
        all_questions = []
        for quiz_idx, quiz in enumerate(session_quizzes):
            for q in quiz['questions']:
                all_questions.append({
                    'quiz_number': quiz_idx + 1,
                    'topic': quiz['topic'],
                    'question': q['question'],
                    'user_answer': q['userAnswer'],
                    'correct_answer': q['correctAnswer'],
                    'is_correct': q['isCorrect'],
                    'time_spent': q['timeSpent'],
                    'timestamp': quiz['timestamp']
                })
        
        df = pd.DataFrame(all_questions)
        
        # Calculate analytics using pandas
        analytics = calculate_analytics(df, session_quizzes)
        
        return analytics
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def calculate_analytics(df, session_quizzes):
    """
    Use pandas to calculate comprehensive analytics
    """
    
    # 1. Overall Performance Metrics
    total_questions = len(df)
    correct_answers = df['is_correct'].sum()
    accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    # 2. Score Distribution (for pie chart)
    score_distribution = {
        'correct': int(correct_answers),
        'incorrect': int(total_questions - correct_answers),
        'accuracy': round(accuracy, 2)
    }
    
    # 3. Performance by Topic (for bar chart)
    topic_performance = df.groupby('topic').agg({
        'is_correct': ['sum', 'count']
    }).reset_index()
    
    topic_performance.columns = ['topic', 'correct', 'total']
    topic_performance['accuracy'] = (topic_performance['correct'] / topic_performance['total'] * 100).round(2)
    
    performance_by_topic = topic_performance.to_dict('records')
    
    # 4. Time Analysis (for bar chart)
    time_analysis = df.groupby('quiz_number')['time_spent'].agg(['mean', 'sum']).reset_index()
    time_analysis.columns = ['quiz_number', 'avg_time', 'total_time']
    time_analysis = time_analysis.round(2)
    
    time_data = time_analysis.to_dict('records')
    
    # 5. Question-by-Question Breakdown
    question_breakdown = df[['question', 'user_answer', 'correct_answer', 'is_correct', 'time_spent']].to_dict('records')
    
    # 6. Progress Over Time (for line chart)
    quiz_scores = []
    for idx, quiz in enumerate(session_quizzes):
        questions = quiz['questions']
        correct = sum(1 for q in questions if q['isCorrect'])
        total = len(questions)
        quiz_scores.append({
            'quiz_number': idx + 1,
            'score': correct,
            'total': total,
            'percentage': round((correct / total * 100) if total > 0 else 0, 2),
            'topic': quiz['topic']
        })
    
    # 7. Time Statistics
    time_stats = {
        'average_time_per_question': round(df['time_spent'].mean(), 2),
        'total_time_spent': round(df['time_spent'].sum(), 2),
        'fastest_question_time': round(df['time_spent'].min(), 2),
        'slowest_question_time': round(df['time_spent'].max(), 2)
    }
    
    # 8. Performance Trends
    df['cumulative_correct'] = df['is_correct'].cumsum()
    df['cumulative_total'] = range(1, len(df) + 1)
    df['cumulative_accuracy'] = (df['cumulative_correct'] / df['cumulative_total'] * 100).round(2)
    
    performance_trend = df[['cumulative_total', 'cumulative_accuracy']].to_dict('records')
    
    return {
        'summary': {
            'total_quizzes': len(session_quizzes),
            'total_questions': total_questions,
            'correct_answers': int(correct_answers),
            'overall_accuracy': round(accuracy, 2)
        },
        'score_distribution': score_distribution,
        'performance_by_topic': performance_by_topic,
        'time_analysis': time_data,
        'time_stats': time_stats,
        'question_breakdown': question_breakdown,
        'quiz_scores': quiz_scores,
        'performance_trend': performance_trend
    }


# Change from @analytics_bp.route to @router.delete
@router.delete('/api/analytics/clear/{session_id}')
async def clear_session(session_id: str):
    """
    Clear session data
    """
    try:
        if session_id in quiz_sessions:
            del quiz_sessions[session_id]
        
        return {
            'success': True,
            'message': 'Session data cleared'
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))