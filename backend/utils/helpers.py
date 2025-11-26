import json
import re
from typing import Optional, Tuple

def parse_JSON_quiz(response_text: str) -> Optional[dict]:
    if not response_text:
        return None
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass
        # Strategy 2: Remove markdown
    cleaned = response_text.strip()
    cleaned = re.sub(r'^```json\\s*', '', cleaned)
    cleaned = re.sub(r'^```\\s*', '', cleaned)
    cleaned = re.sub(r'\\s*```$', '', cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Strategy 3: Extract JSON with regex
    json_match = re.search(r'\\{.*\\}', response_text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

def validate_quiz(quiz_data: dict) -> Tuple[bool,str]:
    if not quiz_data or not isinstance(quiz_data, dict):
        return False, "Invalid quiz data format"

    if 'questions' not in quiz_data:
        return False, "Missing 'questions' field"

    if not isinstance(quiz_data['questions'], list) or len(quiz_data['questions']) == 0:
        return False, "No questions found"
        # Validate each question
    for i, q in enumerate(quiz_data['questions'], 1):
        if 'question' not in q:
            return False, f"Question {i} missing 'question' field"
        if 'options' not in q:
            return False, f"Question {i} missing 'options' field"
        if 'correct_answer' not in q:
            return False, f"Question {i} missing 'correct_answer' field"
        # Check options
        if not all(opt in q['options'] for opt in ['A', 'B', 'C', 'D']):
            return False, f"Question {i} missing required options (A, B, C, D)"
        # Check correct answer
        if q['correct_answer'] not in ['A', 'B', 'C', 'D']:
            return False, f"Question {i} has invalid correct_answer"

    return True, "Valid"

