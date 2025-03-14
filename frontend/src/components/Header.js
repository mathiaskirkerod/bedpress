import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Header = ({ title }) => {
  const { auth, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="bg-white shadow-md p-4 mb-8 rounded-lg">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-xl font-bold text-indigo-600">{title}</h1>
        <div>
          <span className="mr-4 text-gray-600">
            Logged in as: <span className="font-semibold">{auth.name}</span>
          </span>
          <button 
            onClick={handleLogout}
            className="text-red-600 hover:text-red-800"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Header;