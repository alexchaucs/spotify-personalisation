import React from 'react';

const App: React.FC = () => {
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
      // Handle logout success (maybe update state and UI)
    } catch (e) {
      console.error('Error:', e);
    }
  };

  return (
    <div>
      <button onClick={login}>Login</button>
      <button onClick={logout}>Logout</button>
    </div>
  );
};

export default App;
