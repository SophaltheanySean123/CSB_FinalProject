
## Files Created/Modified

### Backend Files:

1. **`backend/utils/quiz_manager.py`** (Enhanced)
   - `QuestionCache` class: Hash Map for O(1) question storage/retrieval
   - `QuizQueue` class: Queue (collections.deque) for FIFO question management
   - `QuizHistory` class: Stack (list) for LIFO quiz attempt tracking
   - `QuizManager` class: Coordinates all data structures

2. **`backend/routes/flask_quiz.py`** (New)
   - Flask blueprint `quiz_bp` with all required endpoints
   - Comprehensive error handling and JSON responses
   - Time complexity documentation

3. **`backend/flask_main.py`** (New)
   - Flask application entry point
   - Registers quiz blueprint
   - CORS configuration for frontend

4. **`backend/requirements.txt`** (Updated)
   - Added Flask and Flask-CORS

### Frontend Files:

1. **`frontend/src/components/QuizRetake.tsx`** (New)
   - Component for quiz retake functionality
   - Statistics display
   - Data structure information box
   - Quiz history visualization

## Data Structures Used

### 1. Hash Map (Dictionary) - QuestionCache
- **Time Complexity**: O(1) for get/set operations
- **Purpose**: Store and retrieve questions by session_id
- **Implementation**: Python dictionary (`dict`)

### 2. Queue (collections.deque) - QuizQueue
- **Time Complexity**: O(1) for enqueue/dequeue operations
- **Purpose**: FIFO (First-In-First-Out) question distribution
- **Implementation**: Python `collections.deque`

### 3. Stack (List) - QuizHistory
- **Time Complexity**: O(1) for push/pop operations
- **Purpose**: LIFO (Last-In-First-Out) quiz attempt tracking
- **Implementation**: Python list with append/pop operations

### 4. Set - Used Questions Tracking
- **Time Complexity**: O(1) for lookup and add operations
- **Purpose**: Track which questions have been used to avoid duplicates
- **Implementation**: Python `set`

## Running the Flask Application

### Option 1: Run Flask App Separately (Port 8001)

```bash
cd CSB_FinalProject/backend
python main.py
```

The Flask API will run on `http://127.0.0.1:8001`

### Option 2: Use FastAPI (Existing - Port 8000)

The existing FastAPI implementation in `routes/quiz.py` already uses the same `quiz_manager` and works with the same endpoints.

## API Endpoints

All endpoints are available under `/api/quiz`:

- **POST** `/api/quiz/upload` - Upload and cache questions (Hash Map)
- **POST** `/api/quiz/generate` - Generate quiz from cache (Queue + Set)
- **POST** `/api/quiz/submit` - Submit results to Stack
- **GET** `/api/quiz/stats/<session_id>` - Get session statistics
- **POST** `/api/quiz/reset` - Reset question pool
- **GET** `/api/quiz/check-cache/<session_id>` - Check cache status

## Frontend Integration

The `QuizRetake.tsx` component is ready to use. To integrate it:

1. Import the component in your main App component
2. Pass `sessionId` and `onStartNewQuiz` callback
3. The component handles all API calls internally

Example usage:
```tsx
import { QuizRetake } from './components/QuizRetake';

// In your component:
<QuizRetake 
  sessionId={sessionId}
  onStartNewQuiz={(questions, numQuestions) => {
    // Handle new quiz generation
    setQuestions(questions);
    setAppState('quiz');
  }}
/>
```

## Time Complexity Summary

| Operation | Data Structure | Time Complexity |
|-----------|---------------|-----------------|
| Store questions | Hash Map | O(n) one-time setup |
| Retrieve questions | Hash Map | O(1) |
| Check cache | Hash Map | O(1) |
| Enqueue question | Queue | O(1) |
| Dequeue question | Queue | O(1) |
| Push quiz result | Stack | O(1) |
| Check used question | Set | O(1) |
| Generate quiz (k questions) | All structures | O(k) |

## Notes

- The Flask blueprint is in `routes/quiz.py` 
- FastAPI implementations use `quiz_manager` 
- The frontend component defaults to FastAPI port (8000) but can be configured
- All data structures maintain O(1) complexity for critical operations

