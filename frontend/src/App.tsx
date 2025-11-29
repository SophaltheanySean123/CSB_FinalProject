import { useState } from 'react';
import { UploadPage } from './components/UploadPage';
import { QuizPage, Question } from './components/QuizPage';
import { ResultsPage } from './components/ResultsPage';

type AppState = 'upload' | 'quiz' | 'results';

export default function App() {
  const [appState, setAppState] = useState<AppState>('upload');
  const [fileName, setFileName] = useState<string>('');
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

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
      setAppState('quiz');
    }
  };

  // Handle quiz submission
  const handleQuizSubmit = (userAnswers: Record<number, string>) => {
    setAnswers(userAnswers);
    setAppState('results');
  };

  // Retry flow
  const handleRetry = () => {
    setAppState('upload');
    setFileName('');
    setQuestions([]);
    setAnswers({});
    setError('');
  };

  return (
    <>
      {loading && <p style={{ padding: '10px', color: 'blue' }}>Generating quiz, please wait...</p>}
      {error && <p style={{ padding: '10px', color: 'red' }}>Error: {error}</p>}

      {appState === 'upload' && (
        <UploadPage onUploadComplete={handleUploadComplete} />
      )}
      {appState === 'quiz' && (
        <QuizPage questions={questions} fileName={fileName} onSubmit={handleQuizSubmit} />
      )}
      {appState === 'results' && (
        <ResultsPage questions={questions} answers={answers} onRetry={handleRetry} />
      )}
    </>
  );
}
