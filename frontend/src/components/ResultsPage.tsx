import { Button } from './ui/button';
import { Card } from './ui/card';
import { CheckCircle, XCircle, Award, RotateCcw } from 'lucide-react';
import { Question } from './QuizPage';

interface ResultsPageProps {
  questions: Question[];
  answers: Record<number, number>;
  onRetry: () => void;
}

export function ResultsPage({ questions, answers, onRetry }: ResultsPageProps) {
  const calculateScore = () => {
    let correct = 0;
    questions.forEach((q) => {
      if (answers[q.id] === q.correctAnswer) {
        correct++;
      }
    });
    return correct;
  };

  const score = calculateScore();
  const percentage = Math.round((score / questions.length) * 100);

  const getScoreColor = () => {
    if (percentage >= 80) return 'text-green-600';
    if (percentage >= 60) return 'text-blue-600';
    if (percentage >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreMessage = () => {
    if (percentage >= 80) return 'Excellent work! 🎉';
    if (percentage >= 60) return 'Good job! 👍';
    if (percentage >= 40) return 'Keep practicing! 📚';
    return 'Need more study time 💪';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Score Card */}
        <Card className="p-8 shadow-lg mb-8 text-center">
          <Award className={`w-20 h-20 mx-auto mb-4 ${getScoreColor()}`} />
          <h1 className="text-4xl mb-2 text-gray-900">Quiz Complete!</h1>
          <p className="text-xl text-gray-600 mb-6">{getScoreMessage()}</p>
          
          <div className={`text-6xl mb-4 ${getScoreColor()}`}>
            {percentage}%
          </div>
          
          <p className="text-xl text-gray-700">
            {score} out of {questions.length} correct
          </p>

          <div className="flex gap-4 justify-center mt-8">
            <Button onClick={onRetry} className="bg-indigo-600 hover:bg-indigo-700 text-white px-8">
              <RotateCcw className="w-4 h-4 mr-2" />
              Start New Quiz
            </Button>
          </div>
        </Card>

        {/* Detailed Results */}
        <div className="space-y-6">
          <h2 className="text-2xl text-gray-900">Review Your Answers</h2>
          
          {questions.map((question, qIndex) => {
            const userAnswer = answers[question.id];
            const isCorrect = userAnswer === question.correctAnswer;
            const wasAnswered = userAnswer !== undefined;

            return (
              <Card key={question.id} className="p-6 shadow-md">
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0 mt-1">
                    {isCorrect ? (
                      <CheckCircle className="w-6 h-6 text-green-600" />
                    ) : (
                      <XCircle className="w-6 h-6 text-red-600" />
                    )}
                  </div>
                  
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-indigo-600">Question {qIndex + 1}</span>
                      {isCorrect ? (
                        <span className="text-green-600 text-sm">Correct</span>
                      ) : (
                        <span className="text-red-600 text-sm">Incorrect</span>
                      )}
                    </div>
                    
                    <h3 className="text-lg text-gray-900 mb-4">{question.question}</h3>
                    
                    <div className="space-y-2">
                      {question.options.map((option, oIndex) => {
                        const isUserAnswer = userAnswer === oIndex;
                        const isCorrectAnswer = oIndex === question.correctAnswer;
                        
                        let bgColor = 'bg-gray-50';
                        let borderColor = 'border-gray-200';
                        let textColor = 'text-gray-700';
                        
                        if (isCorrectAnswer) {
                          bgColor = 'bg-green-50';
                          borderColor = 'border-green-500';
                          textColor = 'text-green-900';
                        } else if (isUserAnswer && !isCorrect) {
                          bgColor = 'bg-red-50';
                          borderColor = 'border-red-500';
                          textColor = 'text-red-900';
                        }
                        
                        return (
                          <div
                            key={oIndex}
                            className={`p-3 rounded-lg border-2 ${bgColor} ${borderColor}`}
                          >
                            <div className="flex items-center justify-between">
                              <span className={textColor}>
                                <span className="mr-2">{String.fromCharCode(65 + oIndex)}.</span>
                                {option}
                              </span>
                              {isCorrectAnswer && (
                                <span className="text-green-600 text-sm ml-2">✓ Correct Answer</span>
                              )}
                              {isUserAnswer && !isCorrectAnswer && (
                                <span className="text-red-600 text-sm ml-2">Your Answer</span>
                              )}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                    
                    {!wasAnswered && (
                      <p className="text-yellow-600 text-sm mt-3">⚠ You did not answer this question</p>
                    )}
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      </div>
    </div>
  );
}
