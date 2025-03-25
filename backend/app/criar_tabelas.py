from app.config import motor, Base
from app.models.models import *

def criar_banco():
    print(Base.metadata.tables.keys())
    Base.metadata.create_all(bind=motor)
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    criar_banco()

