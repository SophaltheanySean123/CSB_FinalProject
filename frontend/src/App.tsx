import { useState } from 'react';
import { UploadPage } from './components/UploadPage';
import { QuizPage, Question } from './components/QuizPage';
import { ResultsPage } from './components/ResultsPage';
import { QuizAnalytics } from './components/QuizAnalytics';

type AppState = 'upload' | 'quiz' | 'results' | 'analytics';

export default function App() {
  const [appState, setAppState] = useState<AppState>('upload');
  const [fileName, setFileName] = useState<string>('');
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [sessionId, setSessionId] = useState<string>('');
  const [quizTiming, setQuizTiming] = useState<any>(null);
  const [topic, setTopic] = useState<string>('General');

  // Call FastAPI /generate_quiz endpoint
  const generateQuizFromBackend = async (file: File, questionCount: number) => {
    try {
      setLoading(true);
      setError('');
      
      const formData = new FormData();
      formData.append('file', file);
      formData.append('num_of_questions', questionCount.toString());
      
      console.log('Uploading file:', file.name, 'Size:', file.size, 'Type:', file.type);
      console.log('Question count:', questionCount);
      
      const response = await fetch('http://127.0.0.1:8000/generate_quiz', {
        method: 'POST',
        body: formData
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: response.statusText }));
        const errorMessage = errorData.detail || response.statusText;
        
        if (response.status === 503 && errorMessage.includes('Rate limit')) {
          throw new Error('⏳ API rate limit reached. Please wait 30 seconds and try again.');
        }
        throw new Error(`Backend error: ${errorMessage}`);
      }
      
      const data = await response.json();
      console.log('Backend response:', data);
      console.log('Questions:', data.questions);
      return data.questions as Question[];
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Failed to generate quiz.');
      return [];
    } finally {
      setLoading(false);
    }
  };

  // Handle upload completion
  const handleUploadComplete = async (file: File, questionCount: number) => {
    setFileName(file.name);
    const generatedQuestions = await generateQuizFromBackend(file, questionCount);
    if (generatedQuestions.length > 0) {
      setQuestions(generatedQuestions);
      // Cache questions in backend with a session id so retake can reuse
      // Reuse existing sessionId if available, otherwise create new one
      const sid = sessionId || `session_${Date.now()}`;
      try {
        await fetch('http://localhost:8000/api/quiz/upload', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ sessionId: sid, questions: generatedQuestions, metadata: { fileName: file.name } })
        });
        setSessionId(sid);
      } catch (e) {
        console.warn('Failed to cache questions on backend', e);
      }
      setAppState('quiz');
    }
  };

  // Handle quiz submission
  const handleQuizSubmit = (payload: { answers: Record<number, string>, start_time?: number, end_time?: number, total_time?: number, per_question_time?: number[], sessionId?: string }) => {
    setAnswers(payload.answers);
    setQuizTiming({ start_time: payload.start_time, end_time: payload.end_time, total_time: payload.total_time, per_question_time: payload.per_question_time });
    if (payload.sessionId) setSessionId(payload.sessionId);
    setAppState('analytics');
  };

  // Retry flow
  const handleRetry = () => {
    setAppState('upload');
    setFileName('');
    setQuestions([]);
    setAnswers({});
    setError('');
    // Don't reset sessionId - keep it to accumulate analytics across retakes
    // setSessionId('');
    setQuizTiming(null);
  };

  // Request a retake using cached questions on backend
  const handleRetakeRequest = async (numQuestions: number) => {
    if (!sessionId) {
      setError('No session available for retake. Please upload a file again.');
      return;
    }

    // Ensure numQuestions is a valid number
    const validNumQuestions = numQuestions && numQuestions > 0 ? numQuestions : 10;
    console.log('Generating retake quiz with', validNumQuestions, 'questions');

    try {
      setLoading(true);
      setError(''); // Clear previous errors
      
      const requestBody = { 
        sessionId, 
        numQuestions: validNumQuestions, 
        allowRepeats: false 
      };
      console.log('Sending request:', requestBody);
      
      const resp = await fetch('http://localhost:8000/api/quiz/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
      });
      
      if (!resp.ok) {
        const errorData = await resp.json().catch(() => ({ error: 'Network error' }));
        throw new Error(errorData.error || `Server error: ${resp.status}`);
      }
      
      const data = await resp.json();
      
      // Check if response has success flag
      if (data.success === false || (!data.success && data.error)) {
        throw new Error(data.error || 'Failed to generate retake quiz');
      }
      
      // Validate questions array
      if (!data.questions || !Array.isArray(data.questions) || data.questions.length === 0) {
        throw new Error(data.error || 'No questions returned from server');
      }
      
      console.log(`Successfully generated ${data.questions.length} questions (requested ${validNumQuestions})`);
      
      // Clear previous answers and reset quiz state
      setQuestions(data.questions);
      setAnswers({});
      setError(''); // Clear any previous errors
      setAppState('quiz');
    } catch (e: any) {
      const errorMessage = e.message || 'Retake failed. Please try again.';
      setError(errorMessage);
      console.error('Retake error:', e);
    } finally {
      setLoading(false);
    }
  };

  // Handle going back to results from analytics
  const handleBackToResults = () => {
    setAppState('results');
  };
  return (
    <>
      {loading && <p style={{ padding: '10px', color: 'blue' }}>Generating quiz, please wait...</p>}
      {error && <p style={{ padding: '10px', color: 'red' }}>Error: {error}</p>}

      {appState === 'upload' && (
        <UploadPage onUploadComplete={handleUploadComplete} />
      )}
      {appState === 'quiz' && (
        <QuizPage questions={questions} fileName={fileName} onSubmit={handleQuizSubmit} sessionId={sessionId} />
      )}
      {appState === 'results' && (
        <ResultsPage questions={questions} answers={answers} onRetry={handleRetry} onRetakeRequest={handleRetakeRequest} />
      )}
      {appState === 'analytics' && (
        <QuizAnalytics
          questions={questions}
          answers={answers}
          topic={topic || 'General'}
          onRetry={handleRetry}
          onBack={handleBackToResults}
          sessionId={sessionId}
          timing={quizTiming}
          onRetakeRequest={handleRetakeRequest}
        />
      )}
    </>
  );
}
