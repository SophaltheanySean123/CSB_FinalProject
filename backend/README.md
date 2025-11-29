quiz-generator/
│
├── main.py                      ← Main FastAPI app (imports routes)
├── .env                         ← API keys
├── requirements.txt             ← Dependencies
│
├── routes/                      ← API Routes
│   ├── __init__.py
│   ├── health.py               ← GET /health
│   └── quiz.py                 ← POST /generate-quiz
│
├── models/                      ← Pydantic Models
│   ├── __init__.py
│   └── schemas.py              ← QuizResponse, QuizQuestion, etc.
│
├── services/                    ← Business Logic
│   ├── __init__.py
│   ├── file_handler.py         ← PDF/DOCX extraction
│   └── quiz_generator.py       ← Gemini AI integration
│
├── utils/                       ← Helper Functions
│   ├── __init__.py
│   └── helpers.py              ← JSON parsing, validation
│
└── temp/                        ← Temporary file storage (auto-created)