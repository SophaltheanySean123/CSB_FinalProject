# Note on Gemini Response Files

Earlier versions of this project saved every raw Gemini API response as a `.json` file in a `gemini_responses/` folder for debugging and auditing purposes. If you do not need this feature, you can safely remove both the folder and the code that writes these files. The current version of the backend no longer generates these files by default.

# How to Run the Project

## 1. Activate the Virtual Environment
```bash
source ./venv/bin/activate
```

## 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## 3. Set Up Environment Variables
- Ensure your `.env` file is present in the `backend` folder with your `GEMINI_API_KEY`.

## 4. Start the Backend Server
```bash
./venv/bin/python main.py
```
or, if you prefer using Uvicorn:
```bash
uvicorn main:app --reload
```

## 5. Start the Frontend Server
```bash
cd frontend
npm run dev
```


