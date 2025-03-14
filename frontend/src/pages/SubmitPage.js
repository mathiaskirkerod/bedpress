import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import Header from '../components/Header';
import TestItem from '../components/TestItem';
import LoadingSpinner from '../components/loadingSpinner';
import { submitSolution } from '../services/api';

const SubmitPage = () => {
  const { auth, logout } = useAuth();
  const [solution, setSolution] = useState('');
  const [feedback, setFeedback] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [lastSubmitTime, setLastSubmitTime] = useState(null);
  const [countdown, setCountdown] = useState(0);
  const navigate = useNavigate();
  
  const testQuestions = [
    "Hvor mange dager må det gå før purregebyr og renter kan beregnes",
    "Legge inn kontaktperson hos kunde",
    "Hvordan trekke en ansatt et beløp i lønn?",
    "HVORDAN FINNER MAN LISTE FOR RF-1321 I TRIPLETEX",
    "Mva på konto uten avdeling"
  ];

  useEffect(() => {
    const verifyAuth = async () => {
      try {
        if (!auth || !auth.isAuthenticated) {
          navigate('/');
        }
      } catch (err) {
        console.error("Authentication verification failed:", err);
        logout();
        navigate('/');
      }
    };

    verifyAuth();
  }, [auth, logout, navigate]);

  useEffect(() => {
    let timer;
    if (countdown > 0) {
      timer = setInterval(() => {
        setCountdown((prevCountdown) => prevCountdown - 1);
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [countdown]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!solution.trim()) {
      setError("Please enter your solution");
      return;
    }

    const now = new Date().getTime();
    if (lastSubmitTime && now - lastSubmitTime < 30000) {
      setError("Please wait 30 seconds before submitting again");
      return;
    }

    setIsSubmitting(true);
    setError(null);
    
    try {
      const response = await submitSolution(auth.name, auth.password, solution);
    
      if (response.status === 401) {
        logout();
        navigate('/');
        return;
      }
    
      const data = await response.json();
      console.log(data);
      setFeedback(data);
      setLastSubmitTime(now);
      setCountdown(30);
    } catch (error) {
      console.error(error);
      setError(error.message || 'Submission failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen p-4">
      <Header title="Submit Your Solution" />

      <div className="max-w-3xl mx-auto bg-white rounded-lg shadow-md overflow-hidden">
        <div className="p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Submit Your Solution</h2>
          
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
              Error: {error}
            </div>
          )}
          
          <form onSubmit={handleSubmit}>
            <div className="mb-6">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="solution">
                Your solution:
              </label>
              <textarea
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                id="solution"
                rows="4"
                placeholder="Enter your solution here..."
                value={solution}
                onChange={(e) => setSolution(e.target.value)}
                required
              />
            </div>
            
            <button
              type="submit"
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-4 rounded-full focus:outline-none focus:shadow-outline flex items-center justify-center"
              disabled={isSubmitting || countdown > 0}
            >
              {isSubmitting ? (
                <>
                  <LoadingSpinner size="md" color="white" />
                  <span className="ml-2">Processing...</span>
                </>
              ) : countdown > 0 ? `Wait ${countdown}s` : 'Submit Solution'}
            </button>
          </form>
          
          <div className="mt-6 border-t pt-4">
            <h3 className="text-lg font-medium text-gray-800 mb-3">Results:</h3>
            <div className="bg-gray-50 p-4 rounded">
              <div className="mb-4">
                <span className="font-semibold">Your Score: </span> 
                <span className={`font-medium text-lg ${feedback && feedback.score > 3 ? 'text-green-600' : 'text-amber-600'}`}>
                  {feedback ? `${feedback.score}/5` : 'N/A'}
                </span>
              </div>
              <div className="mb-6 overflow-hidden rounded-lg border border-gray-200">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Question
                      </th>
                      <th className="py-3 px-4 text-center text-xs font-medium text-gray-500 uppercase tracking-wider w-32">
                        Status
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {testQuestions.map((question, index) => {
                      const result = feedback && feedback.results && feedback.results[index];
                      return (
                        <TestItem 
                          key={index} 
                          question={question}
                          result={result}
                        />
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SubmitPage;