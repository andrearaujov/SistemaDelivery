import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import get_db
from app.models.models import Usuario, Restaurante
from passlib.context import CryptContext

# Configuração para hashing de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Cria o TestClient
@pytest.fixture
def client():
    return TestClient(app)

# Fixture para obter uma sessão do banco de dados
@pytest.fixture(scope="module")
def db_session():
    db = next(get_db())
    yield db
    db.close()

# Fixture para criar um usuário de teste
@pytest.fixture(scope="module")
def test_user(db_session):
    email = "restest@example.com"
    user = db_session.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        hashed_senha = pwd_context.hash("password123")
        user = Usuario(
            nome="Test User",
            email=email,
            senha_hash=hashed_senha,
            telefone="111222333",
            endereco="Rua Teste, 101",
            tipo="consumidor"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
    return user

# Fixture para criar um restaurante de teste associado ao usuário
@pytest.fixture(scope="module")
def test_restaurant(db_session, test_user):
    nome = "Restaurante Teste"
    restaurant = db_session.query(Restaurante).filter(Restaurante.nome == nome).first()
    if not restaurant:
        restaurant = Restaurante(
            dono_id=test_user.id,
            nome=nome,
            cnpj="12345678901234",
            endereco="Rua Restaurante, 456",
            telefone="987654321"
        )
        db_session.add(restaurant)
        db_session.commit()
        db_session.refresh(restaurant)
    return restaurant

# Teste para criar um novo restaurante
def test_create_restaurant(client, test_user):
    restaurant_data = {
        "nome": "Novo Restaurante",
        "cnpj": "763876382",
        "endereco": "Rua Nova, 789",
        "telefone": "123123123",
        "dono_id": test_user.id
    }
    response = client.post("/restaurants/", json=restaurant_data)
    assert response.status_code == 201, f"Erro ao criar restaurante: {response.json()}"
    data = response.json()
    assert data["nome"] == restaurant_data["nome"]
    assert data["cnpj"] == restaurant_data["cnpj"]
    assert data["dono_id"] == test_user.id
    assert "id" in data
    assert "criado_em" in data

# Teste para listar todos os restaurantes
def test_get_restaurants(client):
    response = client.get("/restaurants/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

# Teste para obter um restaurante específico por ID
def test_get_restaurant(client, test_restaurant):
    restaurant_id = test_restaurant.id
    response = client.get(f"/restaurants/{restaurant_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == restaurant_id

# Teste para atualizar um restaurante
def test_update_restaurant(client, test_restaurant):
    restaurant_id = test_restaurant.id
    update_data = {
        "nome": "Restaurante Atualizado",
        "endereco": "Novo Endereço, 100"
    }
    response = client.put(f"/restaurants/{restaurant_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == update_data["nome"]
    assert data["endereco"] == update_data["endereco"]

# Teste para deletar um restaurante
def test_delete_restaurant(client, test_user):
    # Cria um restaurante temporário para exclusão
    temp_data = {
        "nome": "Restaurante Temp",
        "cnpj": "55566677788899",
        "endereco": "Rua Temp, 101",
        "telefone": "000111222",
        "dono_id": test_user.id
    }
    create_resp = client.post("/restaurants/", json=temp_data)
    assert create_resp.status_code == 201, f"Erro ao criar restaurante temporário: {create_resp.json()}"
    restaurant_id = create_resp.json().get("id")
    response = client.delete(f"/restaurants/{restaurant_id}")
    assert response.status_code == 204
    # Verifica se o restaurante foi realmente excluído
    get_resp = client.get(f"/restaurants/{restaurant_id}")
    assert get_resp.status_code == 404
