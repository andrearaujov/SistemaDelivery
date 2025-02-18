from pydantic import BaseModel, EmailStr
from enum import Enum
from datetime import datetime

# Definindo os tipos de usuário possíveis
class TipoUsuario(str, Enum):
    consumidor = "consumidor"
    restaurante = "restaurante"

# Modelo para dados de login
class UsuarioLogin(BaseModel):
    email: str
    senha: str

# Base para os dados do usuário, reutilizável
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: str
    endereco: str
    tipo: TipoUsuario

# Modelo para criação de usuário (inclui a senha)
class UsuarioCreate(UsuarioBase):
    senha: str  # A senha será criptografada no controlador

    class Config:
        orm_mode = True

# Modelo de resposta, inclui ID e data de criação
class UsuarioResponse(UsuarioBase):
    id: int
    criado_em: datetime

    class Config:
        orm_mode = True
