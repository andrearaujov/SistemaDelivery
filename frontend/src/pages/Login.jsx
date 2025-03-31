// src/pages/Login.js
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import LoginForm from '../components/LoginForm';

const Login = () => {
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleLoginSubmit = async (email, password) => {
    try {
      const response = await axios.post('/api/login', { email, password });
      
      localStorage.setItem('token', response.data.token);
      navigate('/profile');  
    } catch (error) {
      setError('Email ou senha incorretos');
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <LoginForm onSubmit={handleLoginSubmit} errorMessage={error} />
    </div>
  );
};

export default Login;
