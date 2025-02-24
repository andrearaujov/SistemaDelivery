import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import get_db
from app.models.models import Usuario, Restaurante, Pedido
from passlib.context import CryptContext

# Cria o TestClient
@pytest.fixture
def client():
    return TestClient(app)

# Cria uma sessão do banco para os testes
@pytest.fixture(scope="module")
def db_session():
    db = next(get_db())
    yield db
    db.close()

# Configuração para hashing de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fixture para criar um usuário de teste
@pytest.fixture(scope="module")
def test_user(db_session):
    email = "testuser@example.com"
    user = db_session.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        hashed_senha = pwd_context.hash("senha123")
        user = Usuario(
            nome="Teste Usuario",
            email=email,
            senha_hash=hashed_senha,
            telefone="123456789",
            endereco="Rua Teste, 123",
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

# Teste para criar um novo pedido
def test_create_order(client, test_user, test_restaurant):
    order_data = {
       "usuario_id": test_user.id,
       "restaurante_id": test_restaurant.id,
       "total": 50.0,
       "status": "pendente"
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 201, f"Erro ao criar pedido: {response.json()}"
    json_resp = response.json()
    assert json_resp["usuario_id"] == test_user.id
    assert json_resp["restaurante_id"] == test_restaurant.id
    assert json_resp["total"] == order_data["total"]
    assert json_resp["status"] == order_data["status"]
    assert "id" in json_resp
    assert "criado_em" in json_resp

# Teste para listar todos os pedidos
def test_get_orders(client):
    response = client.get("/orders/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Teste para obter um pedido específico por ID
def test_get_order(client, test_user, test_restaurant):
    order_data = {
       "usuario_id": test_user.id,
       "restaurante_id": test_restaurant.id,
       "total": 60.0,
       "status": "pendente"
    }
    create_resp = client.post("/orders/", json=order_data)
    created_order = create_resp.json()
    order_id = created_order.get("id")
    if not order_id:
        pytest.fail(f"Pedido não criado corretamente: {create_resp.json()}")
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["id"] == order_id

# Teste para atualizar um pedido
def test_update_order(client, test_user, test_restaurant):
    order_data = {
       "usuario_id": test_user.id,
       "restaurante_id": test_restaurant.id,
       "total": 70.0,
       "status": "pendente"
    }
    create_resp = client.post("/orders/", json=order_data)
    created_order = create_resp.json()
    order_id = created_order.get("id")
    if not order_id:
        pytest.fail(f"Pedido não criado para atualização: {create_resp.json()}")
    
    order_update = {
        "total": 75.0,
        "status": "confirmado"
    }
    response = client.put(f"/orders/{order_id}", json=order_update)
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["total"] == order_update["total"]
    assert json_resp["status"] == order_update["status"]

# Teste para deletar um pedido
def test_delete_order(client, test_user, test_restaurant):
    order_data = {
       "usuario_id": test_user.id,
       "restaurante_id": test_restaurant.id,
       "total": 80.0,
       "status": "pendente"
    }
    create_resp = client.post("/orders/", json=order_data)
    created_order = create_resp.json()
    order_id = created_order.get("id")
    if not order_id:
        pytest.fail(f"Pedido não criado para exclusão: {create_resp.json()}")
    
    response = client.delete(f"/orders/{order_id}")
    assert response.status_code == 204
    get_resp = client.get(f"/orders/{order_id}")
    assert get_resp.status_code == 404
