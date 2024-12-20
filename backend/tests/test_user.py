import pytest
import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base
from app.api.endpoints.user import get_db
from app.api.models import User
import uuid

# Configuração do banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test-dinduo.sqlite"
TEST_DB_PATH = "./test-dinduo.sqlite"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_module(module):
    # Criar banco de dados limpo antes dos testes
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    Base.metadata.create_all(bind=engine)

def teardown_module(module):
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

client = TestClient(app)

def get_unique_email():
    return f"test_{uuid.uuid4().hex[:8]}@example.com"

@pytest.fixture
def test_user():
    user_data = {
        "name": "Test User",
        "email": get_unique_email(),
        "password": "testpassword"
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    return {"user": response.json(), "password": user_data["password"]}

@pytest.fixture
def auth_token(test_user):
    response = client.post(
        "/api/v1/users/token",
        data={
            "username": test_user["user"]["email"],
            "password": test_user["password"]
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return token

@pytest.fixture
def authorized_client(auth_token):
    test_client = TestClient(app)
    test_client.headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    return test_client

def test_create_user():
    response = client.post(
        "/api/v1/users/",
        json={
            "name": "Test User",
            "email": get_unique_email(),
            "password": "testpassword"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert "email" in data
    assert "id" in data

def test_read_users(authorized_client, test_user):
    response = authorized_client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_read_user(authorized_client, test_user):
    response = authorized_client.get(f"/api/v1/users/{test_user['user']['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_user["user"]["name"]
    assert data["email"] == test_user["user"]["email"]

def test_update_user(authorized_client, test_user):
    update_data = {
        "name": "Updated User",
        "email": get_unique_email()
    }
    response = authorized_client.put(
        f"/api/v1/users/{test_user['user']['id']}",
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["email"] == update_data["email"]

"""
def test_delete_user(authorized_client, test_user):
    # Deletar o usuário com o cliente autorizado
    response = authorized_client.delete(f"/api/v1/users/{test_user['user']['id']}")
    assert response.status_code == 204

    # Verificar se o usuário foi deletado usando o mesmo cliente autorizado
    get_response = authorized_client.get(f"/api/v1/users/{test_user['user']['id']}")
    assert get_response.status_code == 404
"""
