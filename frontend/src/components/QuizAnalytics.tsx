import React, { useEffect, useState } from 'react';
import {
  PieChart, Pie, Cell, LineChart, Line,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Download, RotateCcw, ArrowLeft } from 'lucide-react';
import { Question } from './QuizPage';

interface QuizAnalyticsProps {
  questions: Question[];
  answers: Record<number, string>;
  topic?: string;
  onRetry: () => void;
  onBack: () => void;
  sessionId?: string;
  timing?: any;
  onRetakeRequest?: (numQuestions: number) => void;
}

interface AnalyticsData {
  summary: {
    total_quizzes: number;
    total_questions: number;
    correct_answers: number;
    overall_accuracy: number;
  };
  score_distribution: {
    correct: number;
    incorrect: number;
    accuracy: number;
  };
  performance_by_topic: Array<{
    topic: string;
    correct: number;
    total: number;
    accuracy: number;
  }>;
  time_analysis: Array<{
    quiz_number: number;
    avg_time: number;
    total_time: number;
  }>;
  time_stats: {
    average_time_per_question: number;
    total_time_spent: number;
    fastest_question_time: number;
    slowest_question_time: number;
  };
  question_breakdown: Array<{
    question: string;
    user_answer: string;
    correct_answer: string;
    is_correct: boolean;
    time_spent: number;
  }>;
  quiz_scores: Array<{
    quiz_number: number;
    score: number;
    total: number;
    percentage: number;
    topic: string;
  }>;
  performance_trend: Array<{
    cumulative_total: number;
    cumulative_accuracy: number;
  }>;
}

export function QuizAnalytics({
  questions,
  answers,
  topic = 'General',
  onRetry,
  onBack,
  sessionId,
  timing,
  onRetakeRequest
}: QuizAnalyticsProps) {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [retakeCount, setRetakeCount] = useState<number>(Math.min(10, questions.length));
  
  // Generate question breakdown from local questions and answers
  const generateQuestionBreakdown = () => {
    return questions.map((q, idx) => {
      const userAnswer = answers[idx] || 'Not answered';
      const correctAnswer = q.correct_answer;
      const isCorrect = userAnswer === correctAnswer;
      
      // Get the full answer text, not just the key
      const userAnswerText = userAnswer !== 'Not answered' && q.options[userAnswer as keyof typeof q.options]
        ? `${userAnswer}: ${q.options[userAnswer as keyof typeof q.options]}`
        : userAnswer;
      
      const correctAnswerText = q.options[correctAnswer as keyof typeof q.options]
        ? `${correctAnswer}: ${q.options[correctAnswer as keyof typeof q.options]}`
        : correctAnswer;
      
      return {
        question: q.question,
        user_answer: userAnswerText,
        correct_answer: correctAnswerText,
        is_correct: isCorrect,
        time_spent: timing?.per_question_time?.[idx] || 0
      };
    });
  };

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setLoading(true);
        const sid = sessionId || `quiz_${Date.now()}`;

        // Prepare quiz data (include timing if available)
        const quizData: any = {
          sessionId: sid,
          topic,
          questions: questions.map((q, idx) => ({
            question: q.question,
            userAnswer: answers[idx] || 'Not answered',
            correctAnswer: q.correct_answer,
            isCorrect: answers[idx] === q.correct_answer,
            timeSpent: 0
          }))
        };

        if (timing && Array.isArray(timing.per_question_time)) {
          // map timing into question timeSpent
          quizData.questions = quizData.questions.map((q: any, idx: number) => ({ ...q, timeSpent: timing.per_question_time[idx] || 0 }));
          quizData.start_time = timing.start_time;
          quizData.end_time = timing.end_time;
          quizData.total_time = timing.total_time;
        }

        // Submit quiz results to backend analytics
        const submitResponse = await fetch('http://localhost:8000/api/analytics/submit-quiz', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(quizData)
        });

        if (!submitResponse.ok) {
          throw new Error('Failed to submit quiz results');
        }

        // Also submit to quiz submission endpoint for Stack history tracking
        if (sessionId) {
          try {
            const score = questions.filter((q, idx) => answers[idx] === q.correct_answer).length;
            await fetch('http://localhost:8000/api/quiz/submit', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                sessionId: sessionId,
                questions: questions,
                score: score,
                total: questions.length,
                start_time: timing?.start_time,
                end_time: timing?.end_time,
                total_time: timing?.total_time,
                per_question_time: timing?.per_question_time || []
              })
            });
          } catch (err) {
            console.warn('Failed to submit quiz to history stack:', err);
          }
        }

        // Fetch analytics
        const analyticsResponse = await fetch(
          `http://localhost:8000/api/analytics/session/${sessionId}`
        );

        if (!analyticsResponse.ok) {
          throw new Error('Failed to fetch analytics');
        }

        const data = await analyticsResponse.json();
        setAnalyticsData(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
        // Fallback to local analytics calculation
        calculateLocalAnalytics();
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, [questions, answers, topic]);

  const calculateLocalAnalytics = () => {
    // Calculate analytics locally if backend fails
    const correct = questions.filter((q, idx) => answers[idx] === q.correct_answer).length;
    const accuracy = (correct / questions.length) * 100;

    const localData: AnalyticsData = {
      summary: {
        total_quizzes: 1,
        total_questions: questions.length,
        correct_answers: correct,
        overall_accuracy: Math.round(accuracy * 100) / 100
      },
      score_distribution: {
        correct,
        incorrect: questions.length - correct,
        accuracy: Math.round(accuracy * 100) / 100
      },
      performance_by_topic: [
        {
          topic,
          correct,
          total: questions.length,
          accuracy: Math.round(accuracy * 100) / 100
        }
      ],
      time_analysis: [
        {
          quiz_number: 1,
          avg_time: 0,
          total_time: 0
        }
      ],
      time_stats: {
        average_time_per_question: 0,
        total_time_spent: 0,
        fastest_question_time: 0,
        slowest_question_time: 0
      },
      question_breakdown: questions.map((q, idx) => ({
        question: q.question,
        user_answer: answers[idx] || 'Not answered',
        correct_answer: q.correct_answer,
        is_correct: answers[idx] === q.correct_answer,
        time_spent: 0
      })),
      quiz_scores: [
        {
          quiz_number: 1,
          score: correct,
          total: questions.length,
          percentage: Math.round(accuracy * 100) / 100,
          topic
        }
      ],
      performance_trend: questions.map((_, idx) => {
        const correctUpToIndex = questions
          .slice(0, idx + 1)
          .filter((q, i) => answers[i] === q.correct_answer).length;
        return {
          cumulative_total: idx + 1,
          cumulative_accuracy: (correctUpToIndex / (idx + 1)) * 100
        };
      })
    };

    setAnalyticsData(localData);
  };

  const handleExportPDF = () => {
    // Export analytics as CSV
    if (!analyticsData) return;

    const csvContent = [
      ['Quiz Analytics Report'],
      [],
      ['Summary Statistics'],
      ['Total Questions', analyticsData.summary.total_questions],
      ['Correct Answers', analyticsData.summary.correct_answers],
      ['Overall Accuracy %', analyticsData.summary.overall_accuracy],
      [],
      ['Question Details'],
      ['Question', 'User Answer', 'Correct Answer', 'Correct?', 'Time Spent (s)']
    ];

    // Use local question breakdown if analyticsData doesn't have it
    const breakdown = analyticsData.question_breakdown && analyticsData.question_breakdown.length > 0
      ? analyticsData.question_breakdown
      : generateQuestionBreakdown();
    
    breakdown.forEach(q => {
      csvContent.push([
        q.question,
        q.user_answer,
        q.correct_answer,
        q.is_correct ? 'Yes' : 'No',
        (q.time_spent || 0).toString()
      ]);
    });

    const csvString = csvContent.map(row => row.join(',')).join('\n');
    const blob = new Blob([csvString], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `quiz_analytics_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
  };

  const getScoreColor = () => {
    if (!analyticsData) return 'text-gray-600';
    const accuracy = analyticsData.summary.overall_accuracy;
    if (accuracy >= 80) return 'text-green-600';
    if (accuracy >= 60) return 'text-blue-600';
    if (accuracy >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreMessage = () => {
    if (!analyticsData) return 'Loading...';
    const accuracy = analyticsData.summary.overall_accuracy;
    if (accuracy >= 80) return 'Excellent! Outstanding performance! 🎉';
    if (accuracy >= 60) return 'Good job! Keep it up! 👍';
    if (accuracy >= 40) return 'Keep practicing! You\'re getting there! 📚';
    return 'Need more study time! Don\'t give up! 💪';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading analytics...</p>
        </div>
      </div>
    );
  }

  if (!analyticsData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
        <div className="max-w-4xl mx-auto">
          <Card className="p-8 text-center">
            <p className="text-red-600 mb-4">{error || 'Failed to load analytics'}</p>
            <Button onClick={onRetry} className="bg-indigo-600 hover:bg-indigo-700">
              Try Again
            </Button>
          </Card>
        </div>
      </div>
    );
  }


  const accuracy = analyticsData.summary.overall_accuracy;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-gray-900">Quiz Analytics</h1>
            <p className="text-gray-600 mt-2">Detailed performance analysis and insights</p>
          </div>
          <div className="flex gap-3">
            <Button
              onClick={onBack}
              className="bg-gray-600 hover:bg-gray-700 text-white"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back
            </Button>
            <Button
              onClick={handleExportPDF}
              className="bg-green-600 hover:bg-green-700 text-white"
            >
              <Download className="w-4 h-4 mr-2" />
              Export Report
            </Button>
          </div>
        </div>

        {/* Score Summary Card */}
        <Card className="p-8 shadow-lg mb-8 text-center bg-white">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Overall Performance</h2>
          <div className={`text-6xl font-bold mb-4 ${getScoreColor()}`}>
            {accuracy}%
          </div>
          <p className="text-xl text-gray-700 mb-2">
            {analyticsData.summary.correct_answers} out of {analyticsData.summary.total_questions} correct
          </p>
          <p className="text-lg text-gray-600">{getScoreMessage()}</p>
        </Card>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
            {/* Correct vs Incorrect Pie Chart */}
            <Card className="p-6 shadow-lg bg-white">
              <h3 className="text-xl font-bold text-gray-800 mb-4">Correct vs Incorrect</h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={[
                      { name: 'Correct', value: analyticsData.score_distribution.correct },
                      { name: 'Incorrect', value: analyticsData.score_distribution.incorrect }
                    ]}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${name}: ${value}`}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    <Cell fill="#10b981" />
                    <Cell fill="#ef4444" />
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </Card>
        </div>

        {/* Performance Trend */}
        <Card className="p-6 shadow-lg bg-white mb-8">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Performance Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={analyticsData.performance_trend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="cumulative_total" label={{ value: 'Questions', position: 'insideBottomRight', offset: -5 }} />
              <YAxis label={{ value: 'Accuracy %', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="cumulative_accuracy"
                stroke="#8884d8"
                name="Cumulative Accuracy %"
                dot={{ fill: '#8884d8', r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </Card>

        {/* Time Statistics */}
        {analyticsData.time_stats.total_time_spent > 0 && (
          <Card className="p-6 shadow-lg bg-white mb-8">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Time Statistics</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600">Avg Time per Question</p>
                <p className="text-2xl font-bold text-blue-600">{analyticsData.time_stats.average_time_per_question}s</p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600">Total Time Spent</p>
                <p className="text-2xl font-bold text-green-600">{analyticsData.time_stats.total_time_spent}s</p>
              </div>
              <div className="bg-yellow-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600">Fastest Question</p>
                <p className="text-2xl font-bold text-yellow-600">{analyticsData.time_stats.fastest_question_time}s</p>
              </div>
              <div className="bg-red-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600">Slowest Question</p>
                <p className="text-2xl font-bold text-red-600">{analyticsData.time_stats.slowest_question_time}s</p>
              </div>
            </div>
          </Card>
        )}

        {/* Question Breakdown */}
        <Card className="p-6 shadow-lg bg-white">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Question Breakdown</h3>
          <div className="space-y-4">
            {generateQuestionBreakdown().map((item, idx) => (
              <div
                key={idx}
                className={`p-4 rounded-lg border-2 ${
                  item.is_correct ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className="font-semibold text-gray-800 mb-2">
                      Q{idx + 1}: {item.question}
                    </p>
                    <div className="text-sm space-y-1">
                      <p className="text-gray-700">
                        <span className="font-semibold">Your answer:</span> {item.user_answer}
                      </p>
                      <p className={`font-semibold ${item.is_correct ? 'text-green-600' : 'text-red-600'}`}>
                        <span>Correct answer:</span> {item.correct_answer}
                      </p>
                      {item.time_spent > 0 && (
                        <p className="text-gray-500 text-xs mt-1">
                          Time spent: {item.time_spent}s
                        </p>
                      )}
                    </div>
                  </div>
                  <div className="ml-4 flex-shrink-0">
                    {item.is_correct ? (
                      <div className="flex flex-col items-center">
                        <span className="text-2xl">✓</span>
                        <span className="text-sm text-green-600 font-semibold">Correct</span>
                      </div>
                    ) : (
                      <div className="flex flex-col items-center">
                        <span className="text-2xl">✗</span>
                        <span className="text-sm text-red-600 font-semibold">Wrong</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* Action Buttons */}
        <div className="flex gap-4 justify-center mt-8 flex-wrap">
          <Button
            onClick={onRetry}
            className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-3 text-lg"
          >
            <RotateCcw className="w-4 h-4 mr-2" />
            Start New Quiz
          </Button>
          <div className="flex items-center gap-2">
            <input
              type="number"
              min={1}
              max={40}
              step={1}
              value={retakeCount}
              onChange={(e) => {
                const value = e.target.value;
                // Allow empty string for user typing
                if (value === '') {
                  return;
                }
                const numValue = parseInt(value, 10);
                if (!isNaN(numValue)) {
                  // Clamp to valid range
                  const clampedValue = Math.max(1, Math.min(40, numValue));
                  setRetakeCount(clampedValue);
                }
              }}
              onBlur={(e) => {
                const value = e.target.value;
                if (value === '' || isNaN(parseInt(value, 10))) {
                  setRetakeCount(10); // Default to 10 if invalid
                } else {
                  const numValue = parseInt(value, 10);
                  if (numValue < 1) {
                    setRetakeCount(1);
                  } else if (numValue > 40) {
                    setRetakeCount(40);
                  } else {
                    setRetakeCount(numValue);
                  }
                }
              }}
              className="w-20 p-2 border rounded"
            />
            <Button
              onClick={() => {
                console.log('Retake button clicked with count:', retakeCount);
                onRetakeRequest?.(retakeCount);
              }}
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-3 text-lg"
            >
              Retake ({retakeCount})
            </Button>
          </div>
          <Button
            onClick={onBack}
            className="bg-gray-600 hover:bg-gray-700 text-black px-8 py-3 text-lg"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Go Back
          </Button>
        </div>
      </div>
    </div>
  );
}
