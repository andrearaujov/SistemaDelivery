from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator


URL_BANCO_DADOS = "mysql+mysqlconnector://root:Queijominas5*@127.0.0.1/delivery_db"

# Criando a conexão com o banco de dados
motor = create_engine(
    URL_BANCO_DADOS,
    pool_pre_ping=True,
)

SessaoLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor)

Base = declarative_base()


# Função que vai fornecer uma sessão do banco de dados
def get_db() -> Generator[Session, None, None]:
    db = SessaoLocal()
    try:
        yield db
    finally:
        db.close()
