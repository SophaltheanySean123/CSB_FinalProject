import { useState } from 'react';
import { UploadPage } from './components/UploadPage';
import { QuizPage, Question } from './components/QuizPage';
import { ResultsPage } from './components/ResultsPage';

type AppState = 'upload' | 'quiz' | 'results';

// Mock quiz generation function - in production, this would call an AI API
function generateMockQuiz(questionCount: number): Question[] {
  const topics = [
    {
      topic: 'Photosynthesis',
      questions: [
        {
          question: 'What is the primary function of chlorophyll in photosynthesis?',
          options: [
            'To store glucose',
            'To absorb light energy',
            'To release oxygen',
            'To transport water'
          ],
          correctAnswer: 1
        },
        {
          question: 'Which of the following is NOT a product of photosynthesis?',
          options: [
            'Oxygen',
            'Glucose',
            'Carbon dioxide',
            'Water'
          ],
          correctAnswer: 2
        }
      ]
    },
    {
      topic: 'Cell Biology',
      questions: [
        {
          question: 'What is the powerhouse of the cell?',
          options: [
            'Nucleus',
            'Ribosome',
            'Mitochondria',
            'Golgi apparatus'
          ],
          correctAnswer: 2
        },
        {
          question: 'Which organelle is responsible for protein synthesis?',
          options: [
            'Ribosome',
            'Lysosome',
            'Peroxisome',
            'Vacuole'
          ],
          correctAnswer: 0
        }
      ]
    },
    {
      topic: 'Genetics',
      questions: [
        {
          question: 'What does DNA stand for?',
          options: [
            'Deoxyribonucleic Acid',
            'Diribonucleic Acid',
            'Deoxyribonuclear Acid',
            'Dynamic Nuclear Acid'
          ],
          correctAnswer: 0
        },
        {
          question: 'How many chromosomes do humans typically have?',
          options: [
            '23',
            '42',
            '46',
            '48'
          ],
          correctAnswer: 2
        }
      ]
    },
    {
      topic: 'Ecology',
      questions: [
        {
          question: 'What is a primary producer in an ecosystem?',
          options: [
            'Herbivore',
            'Carnivore',
            'Plant',
            'Decomposer'
          ],
          correctAnswer: 2
        },
        {
          question: 'Which process describes the water cycle returning to the atmosphere?',
          options: [
            'Precipitation',
            'Condensation',
            'Evaporation',
            'Filtration'
          ],
          correctAnswer: 2
        }
      ]
    },
    {
      topic: 'Chemistry',
      questions: [
        {
          question: 'What is the chemical symbol for gold?',
          options: [
            'Go',
            'Au',
            'Gd',
            'Ag'
          ],
          correctAnswer: 1
        },
        {
          question: 'What is the pH of a neutral solution?',
          options: [
            '0',
            '7',
            '10',
            '14'
          ],
          correctAnswer: 1
        }
      ]
    },
    {
      topic: 'Physics',
      questions: [
        {
          question: 'What is the speed of light in a vacuum?',
          options: [
            '299,792,458 m/s',
            '300,000 m/s',
            '3,000 km/s',
            '186,000 km/s'
          ],
          correctAnswer: 0
        },
        {
          question: 'What law states that for every action, there is an equal and opposite reaction?',
          options: [
            'First Law of Motion',
            'Second Law of Motion',
            'Third Law of Motion',
            'Law of Gravitation'
          ],
          correctAnswer: 2
        }
      ]
    },
    {
      topic: 'Mathematics',
      questions: [
        {
          question: 'What is the value of π (pi) approximately?',
          options: [
            '3.14',
            '2.71',
            '1.61',
            '4.20'
          ],
          correctAnswer: 0
        },
        {
          question: 'What is the Pythagorean theorem?',
          options: [
            'a + b = c',
            'a² + b² = c²',
            'a × b = c',
            'a² - b² = c²'
          ],
          correctAnswer: 1
        }
      ]
    },
    {
      topic: 'History',
      questions: [
        {
          question: 'In which year did World War II end?',
          options: [
            '1943',
            '1944',
            '1945',
            '1946'
          ],
          correctAnswer: 2
        },
        {
          question: 'Who was the first president of the United States?',
          options: [
            'Thomas Jefferson',
            'George Washington',
            'John Adams',
            'Benjamin Franklin'
          ],
          correctAnswer: 1
        }
      ]
    }
  ];

  const allQuestions: Question[] = [];
  let questionId = 0;

  // Flatten all questions
  topics.forEach(topic => {
    topic.questions.forEach(q => {
      allQuestions.push({
        id: questionId++,
        ...q
      });
    });
  });

  // Shuffle and select the requested number of questions
  const shuffled = allQuestions.sort(() => Math.random() - 0.5);
  return shuffled.slice(0, Math.min(questionCount, allQuestions.length));
}

export default function App() {
  const [appState, setAppState] = useState<AppState>('upload');
  const [fileName, setFileName] = useState<string>('');
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<Record<number, number>>({});

  const handleUploadComplete = (uploadedFileName: string, questionCount: number) => {
    setFileName(uploadedFileName);
    // Simulate quiz generation with a small delay
    setTimeout(() => {
      const generatedQuestions = generateMockQuiz(questionCount);
      setQuestions(generatedQuestions);
      setAppState('quiz');
    }, 1000);
  };

  const handleQuizSubmit = (userAnswers: Record<number, number>) => {
    setAnswers(userAnswers);
    setAppState('results');
  };

  const handleRetry = () => {
    setAppState('upload');
    setFileName('');
    setQuestions([]);
    setAnswers({});
  };

  return (
    <>
      {appState === 'upload' && <UploadPage onUploadComplete={handleUploadComplete} />}
      {appState === 'quiz' && (
        <QuizPage questions={questions} fileName={fileName} onSubmit={handleQuizSubmit} />
      )}
      {appState === 'results' && (
        <ResultsPage questions={questions} answers={answers} onRetry={handleRetry} />
      )}
    </>
  );
}
