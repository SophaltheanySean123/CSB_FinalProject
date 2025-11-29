from google import genai

import os
import time
from services.file_handler import truncate_text
import re
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

# Get API key
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)


def generate_quiz_with_retry(  content:str, num_of_questions: int = 10, max_retries: int = 3) -> dict:
    content = truncate_text(content, max_chars=15000)

    prompt=f"""Based on the following lesson content, generate exactly {num_of_questions} multiple choice questions.

LESSON CONTENT:
{content}

CRITICAL INSTRUCTIONS:
1. Respond ONLY with valid JSON, no markdown code blocks, no additional text
2. Start with {{ and end with }}
3. Generate exactly {num_of_questions} questions
4. Each question must have 4 options (A, B, C, D)
5. Include explanations for correct answers

REQUIRED JSON FORMAT:
{{
  "questions": [
    {{
      "question": "Your question here?",
      "options": {{
        "A": "First option",
        "B": "Second option",
        "C": "Third option",
        "D": "Fourth option"
      }},
      "correct_answer": "A",
      "explanation": "Why this answer is correct"
    }}
  ]
}}
    Generate Quiz now"""

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return {
                "success": True,
                "text": response.text if hasattr(response, 'text') else response.candidates[0].content.parts[0].text,
                "attempt": attempt + 1
            }

        except Exception as e:
            error_msg = str(e)

            # Handle rate limits
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                retry_match = re.search(r'retry in (\\d+\\.?\\d*)s', error_msg)
                wait_time = float(retry_match.group(1)) if retry_match else 30

                if attempt < max_retries - 1:
                    time.sleep(wait_time + 1)
                    continue
                else:
                    return {
                        "success": False,
                        "error": "rate_limit",
                        "message": f"Rate limit exceeded. Please try again in {wait_time:.0f} seconds."
                    }

            # Handle other errors
            return {
                "success": False,
                "error": "api_error",
                "message": f"API error: {error_msg}"
            }

    return {
        "success": False,
        "error": "max_retries",
        "message": "Failed after maximum retries"
    }





