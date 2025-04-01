import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import RegisterForm from '../components/RegisterForm';

const Register = () => {
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const apiUrl = import.meta.env.VITE_API_URL;

  const handleRegisterSubmit = async (nome, email, password, telefone, endereco, tipo) => {
    try {
      const response = await axios.post(`${apiUrl}/users/`, {
        nome,
        email,
        senha: password,
        telefone,
        endereco,
        tipo
      });
      
      if (response.status === 201) {
        navigate('/login');  // Redireciona para a página de login após o cadastro
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Erro ao cadastrar usuário");
    }
  };

  return (
    <div>
      <h2>Cadastro de Usuário</h2>
      <RegisterForm onSubmit={handleRegisterSubmit} errorMessage={error} />
    </div>
  );
};

export default Register;
