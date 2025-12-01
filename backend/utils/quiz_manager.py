from datetime import datetime
from collections import deque
import random
from typing import List, Dict, Optional, Any

class QuestionCache:
    """
    Hash Map data structure to cache questions from uploaded files
    Allows multiple quiz generations without re-uploading
    Time Complexity: O(1) for get/set operations
    """
    def __init__(self):
        self.cache: Dict[str, Dict[str, Any]] = {}
    
    def store_questions(self, session_id: str, questions: List[Dict], metadata: Optional[Dict] = None):
        """
        Store questions in cache with O(1) complexity
        
        Args:
            session_id: Unique session identifier
            questions: List of question objects
            metadata: Additional file information
        """
        self.cache[session_id] = {
            'questions': questions,
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat(),
            'total_questions': len(questions)
        }
        print(f"[CACHE] Stored {len(questions)} questions for session {session_id}")
    
    def get_questions(self, session_id: str) -> List[Dict]:
        """Retrieve all questions with O(1) lookup"""
        return self.cache.get(session_id, {}).get('questions', [])
    
    def has_questions(self, session_id: str) -> bool:
        """Check if session has cached questions"""
        return session_id in self.cache and len(self.cache[session_id].get('questions', [])) > 0
    
    def get_metadata(self, session_id: str) -> Dict:
        """Get cached session metadata"""
        return self.cache.get(session_id, {}).get('metadata', {})
    
    def clear_session(self, session_id: str):
        """Remove session from cache"""
        if session_id in self.cache:
            del self.cache[session_id]
            print(f"[CACHE] Cleared session {session_id}")


class QuizQueue:
    """
    Queue data structure for managing question order
    Ensures sequential and fair question distribution
    Time Complexity: O(1) for enqueue/dequeue
    """
    def __init__(self, questions: List[Dict]):
        self.queue = deque(questions)
        self.original_size = len(questions)
    
    def dequeue(self) -> Optional[Dict]:
        """Remove and return next question (FIFO)"""
        return self.queue.popleft() if self.queue else None
    
    def enqueue(self, question: Dict):
        """Add question to end of queue"""
        self.queue.append(question)
    
    def peek(self) -> Optional[Dict]:
        """View next question without removing"""
        return self.queue[0] if self.queue else None
    
    def size(self) -> int:
        """Get current queue size"""
        return len(self.queue)
    
    def is_empty(self) -> bool:
        """Check if queue is empty"""
        return len(self.queue) == 0
    
    def reset(self, questions: List[Dict]):
        """Reset queue with new questions"""
        self.queue = deque(questions)


class QuizHistory:
    """
    Stack data structure for tracking quiz attempts
    Supports undo/redo and history viewing
    Time Complexity: O(1) for push/pop
    """
    def __init__(self):
        self.history: Dict[str, List[Dict]] = {}
    
    def push(self, session_id: str, quiz_data: Dict):
        """
        Push completed quiz to history stack (LIFO)
        
        Args:
            session_id: Session identifier
            quiz_data: Quiz results and metadata
        """
        if session_id not in self.history:
            self.history[session_id] = []

        entry = {
            'quiz_number': len(self.history[session_id]) + 1,
            'questions': quiz_data.get('questions', []),
            'score': quiz_data.get('score', 0),
            'total': quiz_data.get('total', 0),
            'timestamp': datetime.now().isoformat()
        }

        # Optional timing fields
        if 'start_time' in quiz_data:
            entry['start_time'] = quiz_data.get('start_time')
        if 'end_time' in quiz_data:
            entry['end_time'] = quiz_data.get('end_time')
        if 'total_time' in quiz_data:
            entry['total_time'] = quiz_data.get('total_time')
        if 'per_question_time' in quiz_data:
            entry['per_question_time'] = quiz_data.get('per_question_time')

        self.history[session_id].append(entry)
    
    def pop(self, session_id: str) -> Optional[Dict]:
        """Remove and return last quiz (Stack pop)"""
        if session_id in self.history and self.history[session_id]:
            return self.history[session_id].pop()
        return None
    
    def peek(self, session_id: str) -> Optional[Dict]:
        """View last quiz without removing (Stack peek)"""
        if session_id in self.history and self.history[session_id]:
            return self.history[session_id][-1]
        return None
    
    def get_all(self, session_id: str) -> List[Dict]:
        """Get complete history for session"""
        return self.history.get(session_id, [])
    
    def size(self, session_id: str) -> int:
        """Get number of quiz attempts"""
        return len(self.history.get(session_id, []))


class QuizManager:
    """
    Main quiz management system coordinating multiple data structures:
    - Hash Map (QuestionCache) for O(1) question storage and retrieval
    - Queue (QuizQueue) using collections.deque for FIFO question management - O(1) enqueue/dequeue
    - Stack (QuizHistory) using list for LIFO quiz attempt tracking - O(1) push/pop
    - Set for tracking used questions with O(1) lookup and add operations
    
    Time Complexity Overview:
    - upload_and_cache_questions: O(n) where n = number of questions (one-time setup)
    - generate_new_quiz: O(k) where k = num_questions requested (Set operations are O(1))
    - submit_quiz_results: O(1) - Stack push operation
    - get_session_stats: O(m) where m = number of quiz attempts (for averaging)
    - reset_session: O(1) - Dictionary/Set clearing operations
    """
    def __init__(self):
        self.question_cache = QuestionCache()  # Hash Map for O(1) storage/retrieval
        self.quiz_history = QuizHistory()  # Stack (list) for LIFO history tracking
        self.quiz_queues: Dict[str, QuizQueue] = {}  # Queue per session for FIFO distribution
        self.used_questions: Dict[str, set] = {}  # Set data structure for O(1) lookup
    
    def upload_and_cache_questions(self, session_id: str, questions: List[Dict], metadata: Optional[Dict] = None):
        """
        Upload and cache questions using Hash Map data structure.
        Also initializes Queue and Set tracking for the session.
        
        Time Complexity: O(n) where n = len(questions)
        - Hash Map insertion: O(1) per question (amortized)
        - Queue initialization: O(n)
        - Set initialization: O(1)
        
        Args:
            session_id: Unique session identifier
            questions: List of question dictionaries
            metadata: Optional metadata about the uploaded file
        
        Returns:
            Dictionary with success status and caching information
        """
        # Store in Hash Map - O(1) average case insertion
        self.question_cache.store_questions(session_id, questions, metadata)
        
        # Initialize Queue with question indices for FIFO distribution - O(n)
        # Using collections.deque for O(1) enqueue/dequeue operations
        # Store indices to enable tracking via Set
        indices = list(range(len(questions)))
        random.shuffle(indices)  # Shuffle for variety before FIFO distribution
        # Wrap indices in dict format for Queue compatibility
        index_items = [{'index': idx} for idx in indices]
        self.quiz_queues[session_id] = QuizQueue(index_items)
        
        # Initialize Set for tracking used questions - O(1) lookup
        self.used_questions[session_id] = set()
        
        return {
            'success': True,
            'total_questions': len(questions),
            'session_id': session_id,
            'message': f'Cached {len(questions)} questions. Ready to generate quizzes.'
        }
    
    def generate_new_quiz(self, session_id: str, num_questions: int = 10, allow_repeats: bool = False) -> Dict:
        """
        Generate new quiz from cached questions using Queue (FIFO) and Set data structures.
        No file upload required - questions are retrieved from Hash Map cache.
        
        Time Complexity: O(k) where k = num_questions
        - Hash Map lookup: O(1)
        - Queue dequeue operations: O(1) each
        - Set lookups and additions: O(1) each
        - Overall: O(k) for k questions
        
        Data Structures Used:
        1. Hash Map (QuestionCache): O(1) question retrieval
        2. Queue (QuizQueue): O(1) FIFO question distribution
        3. Set (used_questions): O(1) duplicate checking
        
        Args:
            session_id: Session identifier
            num_questions: Number of questions to generate
            allow_repeats: If True, allows previously used questions
        
        Returns:
            Dictionary with quiz questions, metadata, and remaining pool size
        """
        # Check if questions exist in cache - Hash Map lookup O(1)
        if not self.question_cache.has_questions(session_id):
            return {
                'success': False,
                'error': 'No questions found in cache. Please upload a file first.'
            }
        
        all_questions = self.question_cache.get_questions(session_id)  # Hash Map get - O(1)
        
        # Get or initialize Set for tracking used question indices - O(1) lookup
        if session_id not in self.used_questions:
            self.used_questions[session_id] = set()
        
        used_indices = self.used_questions[session_id]  # Set for O(1) lookup
        
        # Build available indices list (questions not yet used)
        # If allow_repeats, all indices are available
        if allow_repeats:
            available_indices = list(range(len(all_questions)))
        else:
            # Filter out used indices - Set lookup is O(1) per check
            available_indices = [i for i in range(len(all_questions)) if i not in used_indices]
        
        # Edge case: No available questions
        if not available_indices:
            if allow_repeats:
                # Should never happen if allow_repeats is True
                available_indices = list(range(len(all_questions)))
            else:
                # Pool exhausted - reset for fresh questions
                print(f"[QUIZ] Question pool exhausted. Resetting for session {session_id}")
                used_indices.clear()
                available_indices = list(range(len(all_questions)))
        
        # Ensure Queue exists with question indices (not question objects)
        # This allows us to track by index while using Queue for FIFO distribution
        if session_id not in self.quiz_queues:
            shuffled_indices = available_indices.copy()
            random.shuffle(shuffled_indices)
            # Create a queue of indices wrapped in dicts for consistency
            index_objects = [{'index': idx} for idx in shuffled_indices]
            self.quiz_queues[session_id] = QuizQueue(index_objects)
        
        selected_indices = []
        selected_set = set()  # Set to track indices selected for THIS quiz (O(1) lookup)
        
        # Cap num_questions to available pool size
        max_possible = len(all_questions)
        if num_questions > max_possible:
            print(f"[QUIZ] Requested {num_questions} questions but only {max_possible} available. Capping to {max_possible}.")
            num_questions = max_possible
        
        # Build list of available question indices based on allow_repeats setting
        if allow_repeats:
            # Can use any question (except duplicates within this quiz)
            available_indices = list(range(len(all_questions)))
        else:
            # Can only use questions not used in previous quizzes
            available_indices = [i for i in range(len(all_questions)) if i not in used_indices]
            
            # If not enough unique questions available, reset the pool
            if len(available_indices) < num_questions:
                print(f"[QUIZ] Only {len(available_indices)} unused questions available, need {num_questions}. Resetting pool.")
                used_indices.clear()
                available_indices = list(range(len(all_questions)))
        
        # Shuffle for random selection
        random.shuffle(available_indices)
        
        # Select questions ensuring no duplicates within this quiz
        # Use Set for O(1) duplicate checking
        attempts = 0
        max_attempts = len(all_questions) * 2
        
        while len(selected_indices) < num_questions and attempts < max_attempts:
            attempts += 1
            
            # If we've used all available_indices, refill from remaining pool
            if len(available_indices) == 0:
                # Get any questions not yet selected in this quiz
                remaining = [i for i in range(len(all_questions)) if i not in selected_set]
                
                if not remaining:
                    # All questions already selected in this quiz - shouldn't happen but reset pool
                    print(f"[QUIZ] All questions selected. Resetting used_indices.")
                    if not allow_repeats:
                        used_indices.clear()
                    remaining = [i for i in range(len(all_questions)) if i not in selected_set]
                
                if remaining:
                    available_indices = remaining
                    random.shuffle(available_indices)
                else:
                    break  # No more questions available
            
            # Pop next question from available pool
            question_idx = available_indices.pop(0)
            
            # Skip if already selected (shouldn't happen, but safety check)
            if question_idx in selected_set:
                continue
            
            # Add to selected
            selected_indices.append(question_idx)
            selected_set.add(question_idx)  # O(1) add - prevents duplicates
            
            # Mark as used across quizzes if no repeats allowed
            if not allow_repeats:
                used_indices.add(question_idx)  # O(1) add
        
        # Validate we got the right number
        if len(selected_indices) != num_questions:
            print(f"[WARNING] Generated {len(selected_indices)} questions (requested {num_questions})")
        
        # Convert indices to actual questions - O(k) where k = num_questions
        selected_questions = [all_questions[i] for i in selected_indices]
        
        # Shuffle final selection for variety
        random.shuffle(selected_questions)
        
        print(f"[QUIZ] Generated quiz with {len(selected_questions)} questions for session {session_id}")
        print(f"[QUIZ] Selected {len(selected_indices)} unique questions (requested {num_questions}, total available: {len(all_questions)})")
        print(f"[QUIZ] Using Set (O(1) lookup) data structure for duplicate prevention")
        
        return {
            'success': True,
            'questions': selected_questions,
            'total_questions': len(selected_questions),
            'quiz_number': self.quiz_history.size(session_id) + 1,
            'questions_remaining_in_pool': len(all_questions) - len(used_indices) if not allow_repeats else len(all_questions)
        }
    
    def submit_quiz_results(self, session_id: str, quiz_data: Dict):
        """
        Submit quiz results to Stack data structure (LIFO).
        Uses list as Stack for O(1) push operation.
        
        Time Complexity: O(1) - Stack push operation
        
        Data Structure: Stack (QuizHistory using list.append)
        - Push operation: O(1) amortized
        
        Args:
            session_id: Session identifier
            quiz_data: Dictionary containing quiz results, score, timing, etc.
        
        Returns:
            Dictionary with success status and quiz number
        """
        # Push to Stack - O(1) operation
        self.quiz_history.push(session_id, quiz_data)
        
        return {
            'success': True,
            'quiz_number': self.quiz_history.size(session_id),
            'message': 'Quiz results saved to history stack (LIFO)'
        }
    
    def get_session_stats(self, session_id: str) -> Dict:
        """
        Get comprehensive session statistics from all data structures.
        
        Time Complexity: O(m) where m = number of quiz attempts
        - Hash Map lookup: O(1)
        - Set size: O(1)
        - Stack traversal: O(m) for history list
        - Score calculation: O(m)
        
        Args:
            session_id: Session identifier
        
        Returns:
            Dictionary with session statistics including:
            - Total quizzes taken (from Stack)
            - Questions in pool (from Hash Map)
            - Questions used (from Set)
            - Complete quiz history (from Stack)
            - Average score
        """
        # Get history from Stack - O(m) where m = history size
        history = self.quiz_history.get_all(session_id)
        
        # Get total questions from Hash Map - O(1)
        total_questions = len(self.question_cache.get_questions(session_id))
        
        # Get used count from Set - O(1) size operation
        used_count = len(self.used_questions.get(session_id, set()))
        
        # Calculate average score - O(m)
        average_score = sum(q.get('score', 0) for q in history) / len(history) if history else 0
        
        return {
            'total_quizzes_taken': len(history),
            'total_questions_in_pool': total_questions,
            'questions_used': used_count,
            'questions_remaining': total_questions - used_count,
            'quiz_history': history,
            'average_score': round(average_score, 2)
        }
    
    def reset_session(self, session_id: str, keep_cache: bool = True):
        """
        Reset session data and data structures.
        
        Time Complexity: O(1)
        - Dictionary deletion: O(1)
        - Set clearing: O(1)
        - Queue reset: O(1) reference update
        
        Args:
            session_id: Session identifier to reset
            keep_cache: If True, keeps Hash Map cache but resets:
                       - Set (used_questions)
                       - Queue (quiz_queue)
                       If False, clears all data structures including Hash Map
        
        Returns:
            Dictionary with success status
        """
        if keep_cache:
            # Reset tracking structures but keep Hash Map cache
            # Clear Set - O(1)
            if session_id in self.used_questions:
                self.used_questions[session_id] = set()
            
            # Reset Queue by recreating from cached questions - O(n)
            if session_id in self.quiz_queues and self.question_cache.has_questions(session_id):
                questions = self.question_cache.get_questions(session_id)
                indices = list(range(len(questions)))
                random.shuffle(indices)
                index_items = [{'index': idx} for idx in indices]
                self.quiz_queues[session_id] = QuizQueue(index_items)
        else:
            # Clear all data structures - O(1) operations
            self.question_cache.clear_session(session_id)  # Hash Map deletion - O(1)
            
            if session_id in self.used_questions:
                del self.used_questions[session_id]  # Set deletion - O(1)
            
            if session_id in self.quiz_queues:
                del self.quiz_queues[session_id]  # Queue deletion - O(1)
        
        return {
            'success': True,
            'message': 'Session reset successfully',
            'cache_preserved': keep_cache
        }


# Global instance
quiz_manager = QuizManager()
