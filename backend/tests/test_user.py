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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configuração do banco de dados de teste
SQLALCHEMY_DATABASE_URL = "sqlite:///./test-dinduo.sqlite"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_user():
    response = client.post(
        "/api/v1/users/",
        json={"name": "Test User", "email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_read_users():
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_read_user():
    # Primeiro, criamos um usuário
    create_response = client.post(
        "/api/v1/users/",
        json={"name": "Read Test User", "email": "readtest@example.com", "password": "testpassword"}
    )
    user_id = create_response.json()["id"]

    # Agora, lemos o usuário criado
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Read Test User"
    assert data["email"] == "readtest@example.com"

def test_update_user():
    # Primeiro, criamos um usuário
    create_response = client.post(
        "/api/v1/users/",
        json={"name": "Update Test User", "email": "updatetest@example.com", "password": "testpassword"}
    )
    user_id = create_response.json()["id"]

    # Agora, atualizamos o usuário
    update_response = client.put(
        f"/api/v1/users/{user_id}",
        json={"name": "Updated User", "email": "updated@example.com"}
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "Updated User"
    assert data["email"] == "updated@example.com"

def test_delete_user():
    # Primeiro, criamos um usuário
    create_response = client.post(
        "/api/v1/users/",
        json={"name": "Delete Test User", "email": "deletetest@example.com", "password": "testpassword"}
    )
    user_id = create_response.json()["id"]

    # Agora, deletamos o usuário
    delete_response = client.delete(f"/api/v1/users/{user_id}")
    assert delete_response.status_code == 204

    # Verificamos se o usuário foi realmente deletado
    get_response = client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 404


