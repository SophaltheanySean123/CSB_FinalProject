import { useState } from 'react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { RadioGroup, RadioGroupItem } from './ui/radio-group';
import { Label } from './ui/label';
import { Progress } from './ui/progress';
import { Clock } from 'lucide-react';

export interface Question {
  question: string;
  options: {
    A: string;
    B: string;
    C: string;
    D: string;
  };
  correct_answer: string;
  explanation?: string;
}

interface QuizPageProps {
  questions: Question[];
  fileName: string;
  onSubmit: (answers: Record<number, string>) => void;
}

export function QuizPage({ questions, fileName, onSubmit }: QuizPageProps) {
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [currentQuestion, setCurrentQuestion] = useState(0);

  const handleAnswerSelect = (questionIndex: number, answerKey: string) => {
    setAnswers((prev) => ({
      ...prev,
      [questionIndex]: answerKey,
    }));
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleSubmit = () => {
    const unanswered = questions.filter((_, index) => !answers || answers[index] === undefined);
    if (unanswered.length > 0) {
      const confirm = window.confirm(
        `You have ${unanswered.length} unanswered question(s). Do you want to submit anyway?`
      );
      if (!confirm) return;
    }
    onSubmit(answers || {});
  };

  const progress = questions.length > 0 ? ((currentQuestion + 1) / questions.length) * 100 : 0;
  const answeredCount = Object.keys(answers).length;
  const question = questions[currentQuestion];

  // Safety check for empty questions
  if (!questions || questions.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center">
            <h1 className="text-3xl text-gray-900 mb-4">No Questions Available</h1>
            <p className="text-gray-600">There are no questions to display.</p>
          </div>
        </div>
      </div>
    );
  }

  // Safety check for current question
  if (!question) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center">
            <h1 className="text-3xl text-gray-900 mb-4">Question Not Found</h1>
            <p className="text-gray-600">The current question could not be loaded.</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl text-gray-900">Quiz</h1>
              <p className="text-gray-600">Based on: {fileName}</p>
            </div>
            <div className="flex items-center gap-2 bg-white px-4 py-2 rounded-lg shadow">
              <Clock className="w-5 h-5 text-indigo-600" />
              <span className="text-gray-700">
                {answeredCount} / {questions.length} answered
              </span>
            </div>
          </div>
          <Progress value={progress} className="h-2" />
        </div>

        {/* Question Card */}
        <Card className="p-8 shadow-lg mb-6">
          <div className="mb-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-indigo-600 text-sm">
                Question {currentQuestion + 1} of {questions.length}
              </span>
              {answers && answers[currentQuestion] !== undefined && (
                <span className="text-green-600 text-sm">✓ Answered</span>
              )}
            </div>
            <h2 className="text-xl text-gray-900 mb-6">{question.question}</h2>
          </div>

          <RadioGroup
            value={(answers && answers[currentQuestion]) || ""}
            onValueChange={(value: string) => handleAnswerSelect(currentQuestion, value)}
          >
            <div className="space-y-4">
              {question?.options && Object.entries(question.options).map(([key, option]) => (
                <div
                  key={key}
                  className={`flex items-start space-x-3 p-4 rounded-lg border-2 transition-all cursor-pointer ${
                    answers && answers[currentQuestion] === key
                      ? 'border-indigo-500 bg-indigo-50'
                      : 'border-gray-200 hover:border-indigo-300'
                  }`}
                >
                  <RadioGroupItem value={key} id={`option-${key}`} className="mt-1" />
                  <Label
                    htmlFor={`option-${key}`}
                    className="flex-1 cursor-pointer text-gray-800 leading-relaxed"
                  >
                    <span className="mr-2 text-indigo-600">{key}.</span>
                    {option}
                  </Label>
                </div>
              ))}
            </div>
          </RadioGroup>
        </Card>

        {/* Navigation */}
        <div className="flex items-center justify-between">
          <Button
            onClick={handlePrevious}
            disabled={currentQuestion === 0}
            variant="outline"
            className="px-6"
          >
            Previous
          </Button>

          <div className="flex flex-col items-center gap-3">
            {/* Progress indicator */}
            <div className="text-sm text-gray-600">
              Question {currentQuestion + 1} of {questions.length}
            </div>
            
            {/* Question navigation - show only nearby questions for large sets */}
            <div className="flex gap-2 flex-wrap justify-center max-w-md">
              {questions.length <= 10 ? (
                // Show all questions if 10 or fewer
                questions.map((_, index) => (
                  <button
                    key={index}
                    onClick={() => setCurrentQuestion(index)}
                    className={`w-8 h-8 rounded-full text-xs transition-all flex items-center justify-center ${
                      index === currentQuestion
                        ? 'bg-indigo-600 text-white'
                        : answers && answers[index] !== undefined
                        ? 'bg-green-500 text-white'
                        : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
                    }`}
                  >
                    {index + 1}
                  </button>
                ))
              ) : (
                // Show sliding window for more than 10 questions
                (() => {
                  const windowSize = 7;
                  const start = Math.max(0, Math.min(currentQuestion - Math.floor(windowSize / 2), questions.length - windowSize));
                  const end = Math.min(start + windowSize, questions.length);
                  
                  return (
                    <>
                      {/* First question if not in window */}
                      {start > 0 && (
                        <>
                          <button
                            onClick={() => setCurrentQuestion(0)}
                            className={`w-8 h-8 rounded-full text-xs transition-all flex items-center justify-center ${
                              answers && answers[0] !== undefined
                                ? 'bg-green-500 text-white'
                                : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
                            }`}
                          >
                            1
                          </button>
                          {start > 1 && <span className="text-gray-400">...</span>}
                        </>
                      )}
                      
                      {/* Window of questions */}
                      {Array.from({ length: end - start }, (_, i) => start + i).map((index) => (
                        <button
                          key={index}
                          onClick={() => setCurrentQuestion(index)}
                          className={`w-8 h-8 rounded-full text-xs transition-all flex items-center justify-center ${
                            index === currentQuestion
                              ? 'bg-indigo-600 text-white'
                              : answers && answers[index] !== undefined
                              ? 'bg-green-500 text-white'
                              : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
                          }`}
                        >
                          {index + 1}
                        </button>
                      ))}
                      
                      {/* Last question if not in window */}
                      {end < questions.length && (
                        <>
                          {end < questions.length - 1 && <span className="text-gray-400">...</span>}
                          <button
                            onClick={() => setCurrentQuestion(questions.length - 1)}
                            className={`w-8 h-8 rounded-full text-xs transition-all flex items-center justify-center ${
                              currentQuestion === questions.length - 1
                                ? 'bg-indigo-600 text-white'
                                : answers && answers[questions.length - 1] !== undefined
                                ? 'bg-green-500 text-white'
                                : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
                            }`}
                          >
                            {questions.length}
                          </button>
                        </>
                      )}
                    </>
                  );
                })()
              )}
            </div>
          </div>

          {currentQuestion === questions.length - 1 ? (
            <Button onClick={handleSubmit} className="bg-green-600 hover:bg-green-700 text-white px-8">
              Submit Quiz
            </Button>
          ) : (
            <Button onClick={handleNext} className="bg-indigo-600 hover:bg-indigo-700 text-white px-6">
              Next
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
