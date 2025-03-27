// Helper function to get the test icon based on result
export const getTestIcon = (result) => {
  if (result === true) {
    return "✓";
  } else if (result === false) {
    return "✗";
  } else {
    return "?";
  }
};

// Helper function to get the appropriate color class for test results
export const getTestColorClass = (result) => {
  if (result === true) {
    return "bg-green-100 text-green-800";
  } else if (result === false) {
    return "bg-red-100 text-red-800";
  } else {
    return "bg-gray-200 text-gray-500";
  }
};

// Format date for display
export const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString();
};

// Calculate podium height based on score
export const calculatePodiumHeight = (score, place) => {
  switch(place) {
    case 1:
      return `${Math.min(220, score * 22)}px`;
    case 2:
      return `${Math.min(180, score * 20)}px`;
    case 3:
      return `${Math.min(150, score * 18)}px`;
    default:
      return '100px';
  }
};

// Mock data for fallback when API fails
export const getMockLeaderboard = () => {
  return [
    { name: 'user1', score: 9, timestamp: new Date().toISOString() },
    { name: 'user2', score: 8, timestamp: new Date().toISOString() },
    { name: 'user3', score: 5, timestamp: new Date().toISOString() }
  ];
};

export const getMockTop3 = () => {
  return [
    { name: 'user1', score: 9, timestamp: new Date().toISOString() },
    { name: 'user2', score: 8, timestamp: new Date().toISOString() },
    { name: 'user3', score: 7, timestamp: new Date().toISOString() }
  ];
};