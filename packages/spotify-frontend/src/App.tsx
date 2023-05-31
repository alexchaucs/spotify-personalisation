import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import styled from 'styled-components';

const Container = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #282c34;
  color: white;
  font-family: Arial, sans-serif;
  text-align: center;
`;

const Title = styled.h1`
  font-size: 2.5em;
  font-weight: bold;
`;

const Description = styled.p`
  font-size: 1.2em;
  font-weight: bold;
`;

const StyledButton = styled.button`
  background-color: #1DB954; // Spotify green
  color: white;
  border: none;
  padding: 10px 20px;
  margin: 20px;
  font-size: 1em;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;

  &:hover {
    background-color: #1ED760;
  }
`;

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
    <Container>
      <Title>Get Your Spotify Playlist Art Personalised</Title>
      {!isLoggedIn ? (
        <Description>
          Click on the
          <StyledButton onClick={login}>Connect</StyledButton>
          button to begin
        </Description>
      ) : (
        <>
          <Description>You are connected to Spotify!</Description>
          <StyledButton onClick={logout}>Logout</StyledButton>
          <StyledButton onClick={getPlaylist}>Get Playlist</StyledButton>
        </>
      )}
    </Container>
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
