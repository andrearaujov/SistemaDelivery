# backend/app/routers/auth.py
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.models import Usuario
from app.schemas.user import UsuarioCreate, UsuarioResponse, UsuarioLogin
from app.config import SessaoLocal
from datetime import timedelta, datetime, timezone
from jose import JWTError, jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Router de usuários
users_router = APIRouter(prefix="/users", tags=["users"])
# Router de autenticação
auth_router = APIRouter()

# Configurações do JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Dependência para obter a sessão do banco
def get_db():
    db = SessaoLocal()
    try:
        yield db
    finally:
        db.close()

# Função para criar o token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para verificar a senha
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Rota de login
@auth_router.post("/login")
def login_for_access_token(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if not db_usuario or not verify_password(usuario.senha, db_usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_usuario.email}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}




@users_router.post("/", response_model=UsuarioResponse)
def criar_usuario(user: UsuarioCreate, db: Session = Depends(get_db)):
    user_existente = db.query(Usuario).filter(Usuario.email == user.email).first()
    if user_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    hashed_senha = pwd_context.hash(user.senha)
    
    novo_usuario = Usuario(
        nome=user.nome,
        email=user.email,
        senha_hash=hashed_senha,
        telefone=user.telefone,
        endereco=user.endereco,
        tipo=user.tipo
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    return UsuarioResponse(
        id=novo_usuario.id,
        nome=novo_usuario.nome,
        email=novo_usuario.email,
        telefone=novo_usuario.telefone,
        endereco=novo_usuario.endereco,
        tipo=novo_usuario.tipo,
        criado_em=novo_usuario.criado_em
    )
 