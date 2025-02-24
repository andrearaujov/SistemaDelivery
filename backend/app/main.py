# backend/app/main.py
from fastapi import FastAPI
from app.config import motor, Base
from app.routers import auth, users, products, orders  # Adicionando a importação de products
# Criar tabelas no banco
Base.metadata.create_all(bind=motor)

app = FastAPI(title="Sistema de Delivery", version="1.0.0")

# Registrar os routers
app.include_router(users.router)  # Incluindo o router de usuários
app.include_router(auth.auth_router, prefix="/auth", tags=["auth"])  # Incluindo as rotas de autenticação
app.include_router(products.router, prefix="/products", tags=["products"])  # Rota de produtos
app.include_router(orders.router, prefix="/orders", tags=["orders"])  # Rotas de pedidos

@app.get("/")
def root():
    return {"message": "API do Sistema de Delivery está rodando!"}
