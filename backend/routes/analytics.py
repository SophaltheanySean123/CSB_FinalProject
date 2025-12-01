# from fastapi import APIRouter, Request, HTTPException
# from utils.quiz_manager import quiz_manager
# from collections import defaultdict

# router = APIRouter()


# def calculate_analytics(quiz_data: dict) -> dict:
#     """
#     Calculate analytics from quiz data without pandas
#     Uses pure Python with defaultdict and list comprehensions
#     """
#     questions = quiz_data.get('questions', [])
    
#     if not questions:
#         return {
#             'accuracy': 0,
#             'correct': 0,
#             'total': 0,
#             'time_stats': {}
#         }
    
#     correct = sum(1 for q in questions if q.get('isCorrect', False))
#     total = len(questions)
#     accuracy = (correct / total * 100) if total > 0 else 0
    
#     # Calculate timing statistics
#     time_per_question = [q.get('timeSpent', 0) for q in questions if q.get('timeSpent')]
#     time_stats = {}
    
#     if time_per_question:
#         time_stats = {
#             'average_time': sum(time_per_question) / len(time_per_question),
#             'total_time': sum(time_per_question),
#             'min_time': min(time_per_question),
#             'max_time': max(time_per_question)
#         }
    
#     return {
#         'accuracy': round(accuracy, 2),
#         'correct': correct,
#         'total': total,
#         'time_stats': time_stats
#     }


# @router.post('/api/analytics/submit-quiz')
# async def submit_quiz_analytics(request: Request):
#     """
#     Submit quiz results for analytics tracking
#     """
#     try:
#         data = await request.json()
#         session_id = data.get('sessionId')
#         topic = data.get('topic', 'General')
#         questions = data.get('questions', [])
        
#         if not session_id:
#             raise HTTPException(status_code=400, detail='Session ID is required')
        
#         # Calculate analytics
#         analytics = calculate_analytics({'questions': questions})
        
#         # Calculate score
#         score = analytics['correct']
#         total = analytics['total']
        
#         # Store quiz results in history using Stack
#         quiz_data = {
#             'questions': questions,
#             'score': score,
#             'total': total,
#             'start_time': data.get('start_time'),
#             'end_time': data.get('end_time'),
#             'total_time': data.get('total_time'),
#             'per_question_time': data.get('per_question_time', [])
#         }
        
#         result = quiz_manager.submit_quiz_results(session_id, quiz_data)
        
#         return {
#             'success': True,
#             'analytics': analytics,
#             'message': 'Quiz results recorded'
#         }
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.get('/api/analytics/session/{session_id}')
# async def get_session_analytics(session_id: str):
#     """
#     Get comprehensive analytics for a session
#     Uses data from all data structures
#     """
#     try:
#         stats = quiz_manager.get_session_stats(session_id)
        
#         if not stats or stats['total_quizzes_taken'] == 0:
#             raise HTTPException(status_code=404, detail='No quiz data found for this session')
        
#         # Build comprehensive analytics response
#         history = stats.get('quiz_history', [])
        
#         # Calculate overall statistics - sum all questions from all quiz attempts
#         total_correct = sum(q['score'] for q in history)
#         total_questions = sum(q['total'] for q in history)  # Sum actual totals from each quiz attempt
#         overall_accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0
        
#         return {
#             'summary': {
#                 'total_quizzes': stats['total_quizzes_taken'],
#                 'total_questions': stats['total_questions_in_pool'],
#                 'correct_answers': total_correct,
#                 'overall_accuracy': round(overall_accuracy, 2)
#             },
#             'score_distribution': {
#                 'correct': total_correct,
#                 'incorrect': total_questions - total_correct,
#                 'accuracy': round(overall_accuracy, 2)
#             },
#             'performance_by_topic': [
#                 {
#                     'topic': 'General',
#                     'correct': total_correct,
#                     'total': total_questions,
#                     'accuracy': round(overall_accuracy, 2)
#                 }
#             ],
#             'time_analysis': [
#                 {
#                     'quiz_number': i+1,
#                     'avg_time': sum(q.get('per_question_time', [0])) / len(q.get('per_question_time', [1])) if q.get('per_question_time') else 0,
#                     'total_time': q.get('total_time', 0)
#                 }
#                 for i, q in enumerate(history)
#             ],
#             'time_stats': {
#                 'average_time_per_question': 0,
#                 'total_time_spent': sum(q.get('total_time', 0) for q in history),
#                 'fastest_question_time': 0,
#                 'slowest_question_time': 0
#             },
#             'question_breakdown': [],
#             'quiz_scores': [
#                 {
#                     'quiz_number': q.get('quiz_number', i+1),
#                     'score': q.get('score', 0),
#                     'total': q.get('total', 0),
#                     'percentage': (q.get('score', 0) / q.get('total', 1) * 100) if q.get('total') else 0,
#                     'topic': 'General'
#                 }
#                 for i, q in enumerate(history)
#             ],
#             'performance_trend': [
#                 {
#                     'cumulative_total': i+1,
#                     'cumulative_accuracy': ((sum(h.get('score', 0) for h in history[:i+1])) / (sum(h.get('total', 0) for h in history[:i+1])) * 100) if sum(h.get('total', 0) for h in history[:i+1]) > 0 else 0
#                 }
#                 for i in range(len(history))
#             ]
#         }
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
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