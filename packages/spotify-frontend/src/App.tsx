import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from 'react-router-dom';

const App: React.FC = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (location.pathname === '/success') {
      setIsLoggedIn(true);
      navigate('/');
    }
  }, [location, navigate]);

  const login = () => {
    window.location.href = 'http://localhost:5000/login';
  };

  const logout = async () => {
    try {
      const response = await fetch('http://localhost:5000/logout', {
        method: 'GET',
        credentials: 'include', // Send along cookies to the server
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      setIsLoggedIn(false);
    } catch (e) {
      console.error('Error:', e);
    }
  };

  const getPlaylist = async () => {
    try {
      const response = await fetch('http://localhost:5000/get_playlist', {
        method: 'GET',
        credentials: 'include', // Send along cookies to the server
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const playlist = await response.json();
      console.log(playlist);
      // Do something with the playlist
    } catch (e) {
      console.error('Error:', e);
    }
  };
  
  return (
    <div>
      {!isLoggedIn ? (
        <button onClick={login}>Connect</button>
      ) : (
        <>
          <button onClick={logout}>Logout</button>
          <button onClick={getPlaylist}>Get Playlist</button>
        </>
      )}
    </div>
  );
};

export default () => (
  <Router>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/success" element={<App />} />
    </Routes>
  </Router>
);
