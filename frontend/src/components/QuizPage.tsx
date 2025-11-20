import { useState } from 'react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { RadioGroup, RadioGroupItem } from './ui/radio-group';
import { Label } from './ui/label';
import { Progress } from './ui/progress';
import { Clock } from 'lucide-react';

export interface Question {
  id: number;
  question: string;
  options: string[];
  correctAnswer: number;
}

interface QuizPageProps {
  questions: Question[];
  fileName: string;
  onSubmit: (answers: Record<number, number>) => void;
}

export function QuizPage({ questions, fileName, onSubmit }: QuizPageProps) {
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [currentQuestion, setCurrentQuestion] = useState(0);

  const handleAnswerSelect = (questionId: number, answerIndex: number) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: answerIndex,
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
    const unanswered = questions.filter((q) => answers[q.id] === undefined);
    if (unanswered.length > 0) {
      const confirm = window.confirm(
        `You have ${unanswered.length} unanswered question(s). Do you want to submit anyway?`
      );
      if (!confirm) return;
    }
    onSubmit(answers);
  };

  const progress = ((currentQuestion + 1) / questions.length) * 100;
  const answeredCount = Object.keys(answers).length;
  const question = questions[currentQuestion];

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
              {answers[question.id] !== undefined && (
                <span className="text-green-600 text-sm">✓ Answered</span>
              )}
            </div>
            <h2 className="text-xl text-gray-900 mb-6">{question.question}</h2>
          </div>

          <RadioGroup
            value={answers[question.id]?.toString()}
            onValueChange={(value) => handleAnswerSelect(question.id, parseInt(value))}
          >
            <div className="space-y-4">
              {question.options.map((option, index) => (
                <div
                  key={index}
                  className={`flex items-start space-x-3 p-4 rounded-lg border-2 transition-all cursor-pointer ${
                    answers[question.id] === index
                      ? 'border-indigo-500 bg-indigo-50'
                      : 'border-gray-200 hover:border-indigo-300'
                  }`}
                >
                  <RadioGroupItem value={index.toString()} id={`option-${index}`} className="mt-1" />
                  <Label
                    htmlFor={`option-${index}`}
                    className="flex-1 cursor-pointer text-gray-800 leading-relaxed"
                  >
                    <span className="mr-2 text-indigo-600">{String.fromCharCode(65 + index)}.</span>
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

          <div className="flex gap-2">
            {questions.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentQuestion(index)}
                className={`w-8 h-8 rounded-full text-sm transition-all flex items-center justify-center ${
                  index === currentQuestion
                    ? 'bg-indigo-600 text-white'
                    : answers[questions[index].id] !== undefined
                    ? 'bg-green-500 text-white'
                    : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
                }`}
              >
                {index + 1}
              </button>
            ))}
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
