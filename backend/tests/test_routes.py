import pytest
from fastapi.testclient import TestClient
from app.main import app  # Importando o app corretamente de dentro de app/main.py

# Teste de exemplo para verificar se o servidor está funcionando
@pytest.fixture
def client():
    client = TestClient(app)
    return client

# Teste básico para verificar o status da aplicação
def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API do Sistema de Delivery está rodando!"}  # Ajustado

# Teste para criar um novo usuário (registro)
def test_create_user(client):
    user_data = {
        "nome": "João Silva Nogueira Matos",
        "email": "joaofelipecarlos@email.com",
        "telefone": "123456789",
        "endereco": "Rua X, 123",
        "tipo": "consumidor",
        "senha": "senha123"
    }
    response = client.post("/users/", json=user_data)  # Corrigido a rota para /users/
    assert response.status_code == 200  # Status de sucesso
    assert response.json()["nome"] == user_data["nome"]
    assert response.json()["email"] == user_data["email"]
    assert "id" in response.json()  # Verifica se o id foi retornado corretamente
    assert "criado_em" in response.json()  # Verifica se a data de criação foi retornada corretamente

# Teste para login (auth)
def test_login(client):
    login_data = {
        "email": "joao@email.com",
        "senha": "senha123"
    }
    response = client.post("/auth/login", json=login_data)  # Ajuste a rota de login conforme sua implementação
    assert response.status_code == 200
    assert "access_token" in response.json()  # Verifique se o token foi gerado
    assert response.json()["token_type"] == "bearer"  # Verifica o tipo de token
