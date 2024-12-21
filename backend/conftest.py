import pytest
import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base
from app.api.endpoints.user import get_db
import uuid

# Adiciona o diretório raiz do projeto ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

# Configuração do banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test-dinduo.sqlite"
TEST_DB_PATH = "./test-dinduo.sqlite"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Criar banco de dados limpo antes dos testes
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    Base.metadata.create_all(bind=engine)
    yield
    # Limpar banco de dados após os testes
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    return TestClient(app)

def get_unique_email():
    return f"test_{uuid.uuid4().hex[:8]}@example.com"

@pytest.fixture
def test_user(client):
    user_data = {
        "name": "Test User",
        "email": get_unique_email(),
        "password": "testpassword"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    return {"user": response.json(), "password": user_data["password"]}

@pytest.fixture
def auth_token(client, test_user):
    response = client.post(
        "/api/v1/users/token",
        data={
            "username": test_user["user"]["email"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture
def authorized_client(client, auth_token):
    client.headers = {"Authorization": f"Bearer {auth_token}"}
    return client
