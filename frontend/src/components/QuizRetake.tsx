import React, { useState, useEffect } from 'react';

interface QuizRetakeProps {
  sessionId: string;
  onStartNewQuiz: (questions: any[]) => void;
}

const QuizRetake: React.FC<QuizRetakeProps> = ({ sessionId, onStartNewQuiz }) => {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [hasCache, setHasCache] = useState(false);

  useEffect(() => {
    checkCache();
    loadStats();
  }, [sessionId]);

  const checkCache = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/quiz/check-cache/${sessionId}`);
      const data = await response.json();
      setHasCache(data.has_cache);
    } catch (error) {
      console.error('Error checking cache:', error);
    }
  };

  const loadStats = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/quiz/stats/${sessionId}`);
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const handleStartNewQuiz = async (numQuestions: number = 10) => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/quiz/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: sessionId,
          numQuestions: numQuestions,
          allowRepeats: false
        })
      });

      const data = await response.json();

      if (data.success) {
        onStartNewQuiz(data.questions);
      } else {
        alert(data.error || 'Failed to generate quiz');
      }
    } catch (error) {
      console.error('Error generating quiz:', error);
      alert('Failed to generate new quiz');
    } finally {
      setLoading(false);
    }
  };

  const handleResetPool = async () => {
    if (!confirm('Reset question pool? This will allow you to retake all questions.')) {
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/api/quiz/reset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sessionId: sessionId,
          keepCache: true
        })
      });

      const data = await response.json();
      if (data.success) {
        alert('Question pool reset! You can now retake all questions.');
        loadStats();
      }
    } catch (error) {
      console.error('Error resetting pool:', error);
    }
  };

  if (!hasCache) {
    return (
      <div className="text-center p-8 bg-white rounded-lg shadow">
        <div className="text-6xl mb-4">📄</div>
        <h3 className="text-xl font-bold text-gray-800 mb-2">No Questions Cached</h3>
        <p className="text-gray-600">Please upload a file first to start taking quizzes.</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-8">
      {/* Stats Overview */}
      {stats && (
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <h2 className="text-3xl font-bold text-gray-800 mb-6">📊 Session Statistics</h2>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
            <StatCard
              icon="🎯"
              label="Quizzes Taken"
              value={stats.total_quizzes_taken}
              color="bg-blue-500"
            />
            <StatCard
              icon="📚"
              label="Total Questions"
              value={stats.total_questions_in_pool}
              color="bg-green-500"
            />
            <StatCard
              icon="✅"
              label="Questions Used"
              value={stats.questions_used}
              color="bg-purple-500"
            />
            <StatCard
              icon="🔄"
              label="Questions Left"
              value={stats.questions_remaining}
              color="bg-orange-500"
            />
          </div>

          {stats.average_score > 0 && (
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 mb-1">Average Score</p>
                  <p className="text-4xl font-bold text-blue-600">
                    {stats.average_score.toFixed(1)}%
                  </p>
                </div>
                <div className="text-6xl">📈</div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Action Buttons */}
      <div className="bg-white rounded-2xl shadow-xl p-8">
        <h3 className="text-2xl font-bold text-gray-800 mb-6">What would you like to do?</h3>
        
        <div className="space-y-4">
          {/* Start New Quiz */}
          <button
            onClick={() => handleStartNewQuiz(10)}
            disabled={loading || (stats && stats.questions_remaining === 0)}
            className="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-bold py-4 px-6 rounded-xl shadow-lg transition transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Generating...
              </span>
            ) : stats && stats.questions_remaining === 0 ? (
              '🚫 All Questions Used - Reset Pool Below'
            ) : (
              '🎯 Start New Quiz (10 Questions)'
            )}
          </button>

          {/* Quick Quiz Options */}
          <div className="grid grid-cols-3 gap-4">
            <button
              onClick={() => handleStartNewQuiz(5)}
              disabled={loading || (stats && stats.questions_remaining === 0)}
              className="bg-green-500 hover:bg-green-600 text-white font-semibold py-3 px-4 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              ⚡ Quick Quiz (5)
            </button>
            <button
              onClick={() => handleStartNewQuiz(15)}
              disabled={loading || (stats && stats.questions_remaining === 0)}
              className="bg-purple-500 hover:bg-purple-600 text-white font-semibold py-3 px-4 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              📚 Long Quiz (15)
            </button>
            <button
              onClick={() => handleStartNewQuiz(20)}
              disabled={loading || (stats && stats.questions_remaining === 0)}
              className="bg-red-500 hover:bg-red-600 text-white font-semibold py-3 px-4 rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              🔥 Marathon (20)
            </button>
          </div>

          {/* Reset Pool */}
          <div className="border-t pt-4 mt-4">
            <button
              onClick={handleResetPool}
              className="w-full bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-3 px-6 rounded-lg transition"
            >
              🔄 Reset Question Pool (Allow Repeats)
            </button>
          </div>
        </div>

        {/* Info Box */}
        <div className="mt-6 bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
          <div className="flex items-start">
            <span className="text-2xl mr-3">💡</span>
            <div>
              <h4 className="font-bold text-blue-800 mb-1">Using Data Structures</h4>
              <p className="text-sm text-blue-700">
                • <strong>Hash Map:</strong> Stores your uploaded questions for instant access<br />
                • <strong>Queue:</strong> Manages question order and distribution<br />
                • <strong>Set:</strong> Tracks used questions to avoid repeats<br />
                • <strong>Stack:</strong> Keeps history of all your quiz attempts
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Quiz History */}
      {stats && stats.quiz_history && stats.quiz_history.length > 0 && (
        <div className="bg-white rounded-2xl shadow-xl p-8 mt-8">
          <h3 className="text-2xl font-bold text-gray-800 mb-6">📜 Quiz History</h3>
          <div className="space-y-3">
            {stats.quiz_history.map((quiz: any, index: number) => (
              <div
                key={index}
                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
              >
                <div className="flex items-center space-x-4">
                  <div className="bg-blue-500 text-white w-10 h-10 rounded-full flex items-center justify-center font-bold">
                    {quiz.quiz_number}
                  </div>
                  <div>
                    <p className="font-semibold text-gray-800">
                      Quiz #{quiz.quiz_number}
                    </p>
                    <p className="text-sm text-gray-600">
                      {new Date(quiz.timestamp).toLocaleString()}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-gray-800">
                    {quiz.score}/{quiz.total}
                  </p>
                  <p className="text-sm text-gray-600">
                    {((quiz.score / quiz.total) * 100).toFixed(1)}%
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// Helper Component
const StatCard: React.FC<{
  icon: string;
  label: string;
  value: number;
  color: string;
}> = ({ icon, label, value, color }) => (
  <div className="bg-white rounded-xl shadow-lg p-6 text-center hover:shadow-xl transition">
    <div className={`${color} w-14 h-14 rounded-full flex items-center justify-center text-3xl mx-auto mb-3`}>
      {icon}
    </div>
    <p className="text-gray-600 text-sm mb-1">{label}</p>
    <p className="text-3xl font-bold text-gray-800">{value}</p>
  </div>
);

export default QuizRetake;
