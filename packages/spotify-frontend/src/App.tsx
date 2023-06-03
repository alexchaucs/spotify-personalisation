import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import styled from 'styled-components';

interface Playlist {
  name: string;
  url: string;
  description: string;
}

const PlaylistContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
`;

const PlaylistCard = styled.div`
  width: 300px;
  margin: 15px;
  text-align: center;
`;

const PlaylistImage = styled.img`
  width: 100%;
  height: auto;
  max-height: 300px;
  object-fit: cover;
`;

const PlaylistDescription = styled.p`
  font-size: 0.9em;
`;
const Container = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh; // This line is updated
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
  const [playlists, setPlaylists] = useState<Playlist[]>([]);
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
      const response = await fetch('http://localhost:5000/playlists/images', {
        method: 'GET',
        credentials: 'include', // Send along cookies to the server
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const playlists = await response.json();
      setPlaylists(playlists); // Set the state to the fetched playlists
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
          <PlaylistContainer>
            {playlists.map((playlist, index) => (
              <PlaylistCard key={index}>
                <PlaylistImage src={playlist.url} alt={playlist.name} />
                <h2>{playlist.name}</h2>
                <PlaylistDescription>{playlist.description}</PlaylistDescription>
              </PlaylistCard>
            ))}
          </PlaylistContainer>
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
