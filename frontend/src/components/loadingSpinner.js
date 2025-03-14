// src/components/LoadingSpinner.js
import React from 'react';

const LoadingSpinner = ({ size = 'md', color = 'white' }) => {
  const getSize = () => {
    switch (size) {
      case 'sm':
        return 'h-4 w-4';
      case 'lg':
        return 'h-8 w-8';
      case 'xl':
        return 'h-12 w-12';
      default:
        return 'h-5 w-5';
    }
  };

  const getColor = () => {
    switch (color) {
      case 'indigo':
        return 'text-indigo-600';
      case 'gray':
        return 'text-gray-600';
      default:
        return 'text-white';
    }
  };

  return (
    <svg className={`animate-spin ${getSize()} ${getColor()}`} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
  );
};

export default LoadingSpinner;
