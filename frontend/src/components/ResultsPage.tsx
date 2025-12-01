import React from 'react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { CheckCircle, XCircle, Award, RotateCcw, Download } from 'lucide-react';
import { Question } from './QuizPage';
import { saveAs } from 'file-saver';
import Papa from 'papaparse';

interface ResultsPageProps {
  questions: Question[];
  answers: Record<number, string>;
  onRetry: () => void;
  onRetakeRequest?: (numQuestions: number) => void;
}

export function ResultsPage({ questions, answers, onRetry, onRetakeRequest }: ResultsPageProps) {
  const calculateScore = () => {
    let correct = 0;
    questions.forEach((q, index) => {
      if (answers[index] === q.correct_answer) {
        correct++;
      }
    });
    return correct;
  };

  const score = calculateScore();
  const percentage = Math.round((score / questions.length) * 100);

  // Export as JSON
  const handleExportJSON = () => {
    const exportData = questions.map((q, idx) => ({
      question: q.question,
      options: q.options,
      correct_answer: q.correct_answer,
      user_answer: answers[idx] || '',
      explanation: q.explanation || '',
    }));
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    saveAs(blob, 'quiz_results.json');
  };

  // Export as CSV
  const handleExportCSV = () => {
    const exportData = questions.map((q, idx) => ({
      question: q.question,
      option_A: q.options.A,
      option_B: q.options.B,
      option_C: q.options.C,
      option_D: q.options.D,
      correct_answer: q.correct_answer,
      user_answer: answers[idx] || '',
      explanation: q.explanation || '',
    }));
    const csv = Papa.unparse(exportData);
    const blob = new Blob([csv], { type: 'text/csv' });
    saveAs(blob, 'quiz_results.csv');
  };

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
            <Button onClick={handleExportJSON} className="bg-green-600 hover:bg-green-700 text-white px-8" title="Export as JSON">
              <Download className="w-4 h-4 mr-2" />
              Export JSON
            </Button>
            <Button onClick={handleExportCSV} className="bg-blue-600 hover:bg-blue-700 text-white px-8" title="Export as CSV">
              <Download className="w-4 h-4 mr-2" />
              Export CSV
            </Button>
          </div>
        </Card>

        {/* Detailed Results */}
        <div className="space-y-6">
          <h2 className="text-2xl text-gray-900">Review Your Answers</h2>
          
          {questions.map((question, qIndex) => {
            const userAnswer = answers[qIndex];
            const isCorrect = userAnswer === question.correct_answer;
            const wasAnswered = userAnswer !== undefined;

            return (
              <Card key={qIndex} className="p-6 shadow-md">
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
                      {Object.entries(question.options).map(([key, option]) => {
                        const isUserAnswer = userAnswer === key;
                        const isCorrectAnswer = key === question.correct_answer;
                        
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
                            key={key}
                            className={`p-3 rounded-lg border-2 ${bgColor} ${borderColor}`}
                          >
                            <div className="flex items-center justify-between">
                              <span className={textColor}>
                                <span className="mr-2">{key}.</span>
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
