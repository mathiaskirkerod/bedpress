// Use relative URLs for same-origin API calls
export const loginUser = async (name, password) => {
  const response = await fetch(`/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ name, password }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Login failed');
  }

  return await response.json();
};

export const submitSolution = async (name, password, solution) => {
  const response = await fetch(`/submit`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ name, solution }), // password, 
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Submission failed');
  }
  return await response.json();
};

export const getLeaderboard = async () => {
  const response = await fetch(`/leaderboard`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch leaderboard');
  }
  
  return await response.json();
};

export const getTop3 = async () => {
  const response = await fetch(`/top3`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch top 3');
  }
  
  return await response.json();
};

export const getFinalLeaderboard = async () => {
  const response = await fetch(`/final`);
  if (!response.ok) {
    throw new Error('Failed to fetch final leaderboard');
  }
  return await response.json();
};