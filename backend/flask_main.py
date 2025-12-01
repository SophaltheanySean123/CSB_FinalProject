"""
Flask application entry point for Quiz API.

This Flask app uses advanced data structures:
- Hash Map for O(1) question storage/retrieval
- Queue (collections.deque) for FIFO question distribution
- Stack (list) for LIFO quiz attempt tracking
- Set for O(1) used question tracking

To run: python flask_main.py
"""

from flask import Flask
from flask_cors import CORS
from routes.flask_quiz import quiz_bp
import os
from dotenv import load_dotenv

load_dotenv()

# Verify API key exists
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not found in the env")

app = Flask(__name__)

# Enable CORS for frontend communication
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Register the quiz blueprint
app.register_blueprint(quiz_bp)

@app.route('/')
def root():
    """API information endpoint"""
    return {
        "service": "AI GENERATED QUIZ - Flask API",
        "version": "1.0.0",
        "status": "online",
        "framework": "Flask",
        "data_structures": {
            "hash_map": "QuestionCache - O(1) storage/retrieval",
            "queue": "QuizQueue (deque) - O(1) FIFO operations",
            "stack": "QuizHistory (list) - O(1) LIFO operations",
            "set": "used_questions - O(1) lookup"
        },
        "endpoints": {
            "POST /api/quiz/upload": "Upload and cache questions (Hash Map)",
            "POST /api/quiz/generate": "Generate quiz from cache (Queue + Set)",
            "POST /api/quiz/submit": "Submit results to Stack",
            "GET /api/quiz/stats/<session_id>": "Get session statistics",
            "POST /api/quiz/reset": "Reset question pool",
            "GET /api/quiz/check-cache/<session_id>": "Check cache status (Hash Map lookup)"
        }
    }

@app.route('/health')
def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Quiz API",
        "framework": "Flask"
    }

if __name__ == '__main__':
    # Run Flask development server
    app.run(host='0.0.0.0', port=8001, debug=True)

