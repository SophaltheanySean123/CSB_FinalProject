from fastapi import APIRouter, Request, HTTPException
from utils.quiz_manager import quiz_manager
from collections import defaultdict

router = APIRouter()


def calculate_analytics(quiz_data: dict) -> dict:
    """
    Calculate analytics from quiz data without pandas
    Uses pure Python with defaultdict and list comprehensions
    """
    questions = quiz_data.get('questions', [])
    
    if not questions:
        return {
            'accuracy': 0,
            'correct': 0,
            'total': 0,
            'time_stats': {}
        }
    
    correct = sum(1 for q in questions if q.get('isCorrect', False))
    total = len(questions)
    accuracy = (correct / total * 100) if total > 0 else 0
    
    # Calculate timing statistics
    time_per_question = [q.get('timeSpent', 0) for q in questions if q.get('timeSpent')]
    time_stats = {}
    
    if time_per_question:
        time_stats = {
            'average_time': sum(time_per_question) / len(time_per_question),
            'total_time': sum(time_per_question),
            'min_time': min(time_per_question),
            'max_time': max(time_per_question)
        }
    
    return {
        'accuracy': round(accuracy, 2),
        'correct': correct,
        'total': total,
        'time_stats': time_stats
    }


@router.post('/api/analytics/submit-quiz')
async def submit_quiz_analytics(request: Request):
    """
    Submit quiz results for analytics tracking
    """
    try:
        data = await request.json()
        session_id = data.get('sessionId')
        topic = data.get('topic', 'General')
        questions = data.get('questions', [])
        
        if not session_id:
            raise HTTPException(status_code=400, detail='Session ID is required')
        
        # Calculate analytics
        analytics = calculate_analytics({'questions': questions})
        
        # Calculate score
        score = analytics['correct']
        total = analytics['total']
        
        # Store quiz results in history using Stack
        quiz_data = {
            'questions': questions,
            'score': score,
            'total': total,
            'start_time': data.get('start_time'),
            'end_time': data.get('end_time'),
            'total_time': data.get('total_time'),
            'per_question_time': data.get('per_question_time', [])
        }
        
        result = quiz_manager.submit_quiz_results(session_id, quiz_data)
        
        return {
            'success': True,
            'analytics': analytics,
            'message': 'Quiz results recorded'
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/api/analytics/session/{session_id}')
async def get_session_analytics(session_id: str):
    """
    Get comprehensive analytics for a session
    Uses data from all data structures
    """
    try:
        stats = quiz_manager.get_session_stats(session_id)
        
        if not stats or stats['total_quizzes_taken'] == 0:
            raise HTTPException(status_code=404, detail='No quiz data found for this session')
        
        # Build comprehensive analytics response
        history = stats.get('quiz_history', [])
        
        # Calculate overall statistics - sum all questions from all quiz attempts
        total_correct = sum(q['score'] for q in history)
        total_questions = sum(q['total'] for q in history)  # Sum actual totals from each quiz attempt
        overall_accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0
        
        return {
            'summary': {
                'total_quizzes': stats['total_quizzes_taken'],
                'total_questions': stats['total_questions_in_pool'],
                'correct_answers': total_correct,
                'overall_accuracy': round(overall_accuracy, 2)
            },
            'score_distribution': {
                'correct': total_correct,
                'incorrect': total_questions - total_correct,
                'accuracy': round(overall_accuracy, 2)
            },
            'performance_by_topic': [
                {
                    'topic': 'General',
                    'correct': total_correct,
                    'total': total_questions,
                    'accuracy': round(overall_accuracy, 2)
                }
            ],
            'time_analysis': [
                {
                    'quiz_number': i+1,
                    'avg_time': sum(q.get('per_question_time', [0])) / len(q.get('per_question_time', [1])) if q.get('per_question_time') else 0,
                    'total_time': q.get('total_time', 0)
                }
                for i, q in enumerate(history)
            ],
            'time_stats': {
                'average_time_per_question': 0,
                'total_time_spent': sum(q.get('total_time', 0) for q in history),
                'fastest_question_time': 0,
                'slowest_question_time': 0
            },
            'question_breakdown': [],
            'quiz_scores': [
                {
                    'quiz_number': q.get('quiz_number', i+1),
                    'score': q.get('score', 0),
                    'total': q.get('total', 0),
                    'percentage': (q.get('score', 0) / q.get('total', 1) * 100) if q.get('total') else 0,
                    'topic': 'General'
                }
                for i, q in enumerate(history)
            ],
            'performance_trend': [
                {
                    'cumulative_total': i+1,
                    'cumulative_accuracy': ((sum(h.get('score', 0) for h in history[:i+1])) / (sum(h.get('total', 0) for h in history[:i+1])) * 100) if sum(h.get('total', 0) for h in history[:i+1]) > 0 else 0
                }
                for i in range(len(history))
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
