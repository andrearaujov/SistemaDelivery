from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UsuarioCreate, UsuarioResponse
from app.models.models import Usuario
from app.config import get_db
from passlib.context import CryptContext

router = APIRouter(prefix="/users", tags=["users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/", response_model=UsuarioResponse)
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
    
    return novo_usuario
