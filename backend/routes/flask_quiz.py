"""
Flask Blueprint for Quiz API endpoints using advanced data structures.

This module provides Flask routes for quiz management using:
- Hash Map (QuestionCache) for O(1) question storage/retrieval
- Queue (QuizQueue) for FIFO question distribution
- Stack (QuizHistory) for LIFO quiz attempt tracking
- Set for O(1) used question tracking

Time Complexities:
- POST /api/quiz/upload: O(n) where n = number of questions
- POST /api/quiz/generate: O(k) where k = num_questions requested
- POST /api/quiz/submit: O(1) - Stack push
- GET /api/quiz/stats/<session_id>: O(m) where m = quiz attempts
- POST /api/quiz/reset: O(1)
- GET /api/quiz/check-cache/<session_id>: O(1) - Hash Map lookup
"""

from flask import Blueprint, request, jsonify
from utils.quiz_manager import quiz_manager
from typing import Dict, Any

# Create Flask blueprint named 'quiz_bp'
quiz_bp = Blueprint('quiz', __name__, url_prefix='/api/quiz')


@quiz_bp.route('/upload', methods=['POST'])
def upload_questions():
    """
    Upload and cache questions from file.
    
    Uses Hash Map (QuestionCache) for O(1) storage and retrieval.
    Also initializes Queue and Set tracking for the session.
    
    Expected JSON:
    {
        "sessionId": "string",
        "questions": [...],
        "metadata": {...}  # optional
    }
    
    Returns:
        JSON response with success status and caching information
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        session_id = data.get('sessionId')
        questions = data.get('questions', [])
        metadata = data.get('metadata', {})
        
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'Session ID is required'
            }), 400
        
        if not questions or len(questions) == 0:
            return jsonify({
                'success': False,
                'error': 'Questions array is required and cannot be empty'
            }), 400
        
        # Use QuizManager to cache questions (Hash Map storage)
        result = quiz_manager.upload_and_cache_questions(
            session_id=session_id,
            questions=questions,
            metadata=metadata
        )
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@quiz_bp.route('/generate', methods=['POST'])
def generate_new_quiz():
    """
    Generate new quiz from cached questions without re-uploading file.
    
    Uses:
    - Hash Map: O(1) question retrieval from cache
    - Queue: O(1) FIFO question distribution
    - Set: O(1) duplicate checking
    
    Expected JSON:
    {
        "sessionId": "string",
        "numQuestions": 10,  # optional, default 10
        "allowRepeats": false  # optional, default false
    }
    
    Returns:
        JSON response with quiz questions and metadata
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        session_id = data.get('sessionId')
        num_questions = data.get('numQuestions', 10)
        allow_repeats = data.get('allowRepeats', False)
        
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'Session ID is required'
            }), 400
        
        # Validate num_questions
        if not isinstance(num_questions, int) or num_questions < 1:
            return jsonify({
                'success': False,
                'error': 'numQuestions must be a positive integer'
            }), 400
        
        # Generate quiz using Queue (FIFO) and Set (O(1) lookup)
        result = quiz_manager.generate_new_quiz(
            session_id=session_id,
            num_questions=num_questions,
            allow_repeats=allow_repeats
        )
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@quiz_bp.route('/submit', methods=['POST'])
def submit_quiz_results():
    """
    Submit completed quiz results to Stack (history).
    
    Uses Stack data structure (list) for LIFO quiz attempt tracking.
    Time Complexity: O(1) - Stack push operation
    
    Expected JSON:
    {
        "sessionId": "string",
        "questions": [...],
        "score": 8,
        "total": 10,
        "start_time": 1234567890,  # optional
        "end_time": 1234567900,  # optional
        "total_time": 10,  # optional
        "per_question_time": [...]  # optional
    }
    
    Returns:
        JSON response with success status and quiz number
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        session_id = data.get('sessionId')
        
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'Session ID is required'
            }), 400
        
        # Prepare quiz data for Stack storage
        quiz_data = {
            'questions': data.get('questions', []),
            'score': data.get('score', 0),
            'total': data.get('total', 0),
            'start_time': data.get('start_time'),
            'end_time': data.get('end_time'),
            'total_time': data.get('total_time'),
            'per_question_time': data.get('per_question_time', [])
        }
        
        # Push to Stack - O(1) operation
        result = quiz_manager.submit_quiz_results(session_id, quiz_data)
        
        return jsonify(result), 200
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@quiz_bp.route('/stats/<session_id>', methods=['GET'])
def get_session_stats(session_id: str):
    """
    Get session statistics from all data structures.
    
    Retrieves information from:
    - Hash Map (QuestionCache): Total questions in pool
    - Set (used_questions): Questions used count
    - Stack (QuizHistory): Quiz attempts and scores
    
    Time Complexity: O(m) where m = number of quiz attempts
    
    Args:
        session_id: Session identifier from URL path
    
    Returns:
        JSON response with comprehensive session statistics
    """
    try:
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'Session ID is required'
            }), 400
        
        # Get stats from all data structures
        stats = quiz_manager.get_session_stats(session_id)
        
        return jsonify({
            'success': True,
            **stats
        }), 200
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@quiz_bp.route('/reset', methods=['POST'])
def reset_session():
    """
    Reset session question pool and usage tracking.
    
    Time Complexity: O(1)
    - Dictionary deletion: O(1)
    - Set clearing: O(1)
    
    Expected JSON:
    {
        "sessionId": "string",
        "keepCache": true  # optional, default true
    }
    
    Returns:
        JSON response with success status
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        session_id = data.get('sessionId')
        keep_cache = data.get('keepCache', True)
        
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'Session ID is required'
            }), 400
        
        # Reset session data structures
        result = quiz_manager.reset_session(session_id, keep_cache)
        
        return jsonify(result), 200
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@quiz_bp.route('/check-cache/<session_id>', methods=['GET'])
def check_cache(session_id: str):
    """
    Check if session has cached questions.
    
    Uses Hash Map lookup for O(1) complexity.
    
    Args:
        session_id: Session identifier from URL path
    
    Returns:
        JSON response indicating cache status and metadata
    """
    try:
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'Session ID is required'
            }), 400
        
        # Hash Map lookup - O(1)
        has_cache = quiz_manager.question_cache.has_questions(session_id)
        
        if has_cache:
            questions = quiz_manager.question_cache.get_questions(session_id)  # O(1)
            metadata = quiz_manager.question_cache.get_metadata(session_id)  # O(1)
            
            return jsonify({
                'has_cache': True,
                'total_questions': len(questions),
                'metadata': metadata
            }), 200
        else:
            return jsonify({
                'has_cache': False,
                'message': 'No cached questions found for this session'
            }), 200
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

