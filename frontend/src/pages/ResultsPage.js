// src/pages/ResultsPage.js
import React, { useState, useEffect } from 'react';
import { getLeaderboard, getTop3 } from '../services/api';
import { getMockLeaderboard, getMockTop3 } from '../utils/helpers';
import LoadingSpinner from '../components/loadingSpinner';
import Podium from '../components/Podium';
import LeaderboardTable from '../components/leaderboardTable';
import QRCode from '../components/qrCode';

const ResultsPage = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [top3, setTop3] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch leaderboard data
        const leaderboardData = await getLeaderboard();
        
        // Fetch top 3 data
        const top3Data = await getTop3();
        
        setLeaderboard(leaderboardData);
        setTop3(top3Data);
        setError(null);
      } catch (err) {
        setError(err.message);
        // Use mock data if API fails
        setLeaderboard(getMockLeaderboard());
        setTop3(getMockTop3());
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    
    // Poll for updates every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <LoadingSpinner size="xl" color="indigo" />
          <div className="mt-4 text-xl font-semibold text-indigo-600">Loading results...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-4">
      <div className="container mx-auto max-w-6xl">
        <h1 className="text-3xl font-bold text-center text-indigo-700 mb-8">Competition Results</h1>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            Error: {error}. Showing mock data.
          </div>
        )}
        
        {/* Mock QR Code */}
        <QRCode />
        
        {/* Podium section */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-2xl font-semibold mb-8 text-center">Winners Podium</h2>
          <Podium top3={top3} />
        </div>
        
        {/* Leaderboard section */}
        <LeaderboardTable leaderboard={leaderboard} />
      </div>
    </div>
  );
};

export default ResultsPage;
