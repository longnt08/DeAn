import React, {useState, useEffect} from "react";
import {BrowserRouter as Router, Route, Navigate} from 'react-router-dom';
import axios from 'axios'
import Registration from './components/Registration';
import Login from './components/Login';
import Dashboard from './components/Dashboard'

const App = () => {
  const [token, setToken] = useState(localStorage.getItem('token') || '');

  const login = async (username, password) => {
    const res = await axios.post('/login', {username, password});
    setToken(res.data.token);
    localStorage.setItem('token', res.data.token);
  };
  const logout = () => {
    setToken('');
    localStorage.removeItem('token');
  };
  
  return (
    <Router>
      <Route path="/register" Component={Registration} />
      <Route path="/login">
        <Login login={login} />
      </Route>
      <Route path="/dashboard">
        {token ? <Dashboard token={token} logout={logout} /> : <Navigate to="/login" />}
      </Route>
    </Router>
  );
};

export default App;