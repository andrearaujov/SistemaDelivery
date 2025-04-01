import { useState } from 'react';

const RegisterForm = ({ onSubmit, errorMessage }) => {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [telefone, setTelefone] = useState('');
  const [endereco, setEndereco] = useState('');
  const [tipo, setTipo] = useState('consumidor');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(nome, email, password, telefone, endereco, tipo);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input 
        type="text" 
        value={nome} 
        onChange={(e) => setNome(e.target.value)} 
        placeholder="Nome" 
        required 
      />
      <input 
        type="email" 
        value={email} 
        onChange={(e) => setEmail(e.target.value)} 
        placeholder="Email" 
        required 
      />
      <input 
        type="password" 
        value={password} 
        onChange={(e) => setPassword(e.target.value)} 
        placeholder="Senha" 
        required 
      />
      <input 
        type="text" 
        value={telefone} 
        onChange={(e) => setTelefone(e.target.value)} 
        placeholder="Telefone" 
      />
      <input 
        type="text" 
        value={endereco} 
        onChange={(e) => setEndereco(e.target.value)} 
        placeholder="Endereço" 
      />
      <select value={tipo} onChange={(e) => setTipo(e.target.value)}>
        <option value="consumidor">Consumidor</option>
        <option value="restaurante">Restaurante</option>
      </select>
      <button type="submit">Cadastrar</button>
      {errorMessage && <p>{errorMessage}</p>}
    </form>
  );
};

export default RegisterForm;
