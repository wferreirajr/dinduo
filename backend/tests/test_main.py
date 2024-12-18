from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/api/users/",
        json={"first_name": "Test", "last_name": "User", "email": "test@example.com"}
    )
    assert response.status_code == 201
    assert response.json()["User"]["email"] == "test@example.com"

def test_read_user():
    # Primeiro, crie um usuário
    create_response = client.post(
        "/api/users/",
        json={"first_name": "Read", "last_name": "Test", "email": "read@example.com"}
    )
    user_id = create_response.json()["User"]["id"]
    
    # Agora, leia o usuário
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["User"]["email"] == "read@example.com"

def test_update_user():
    # Primeiro, crie um usuário
    create_response = client.post(
        "/api/users/",
        json={"first_name": "Update", "last_name": "Test", "email": "update@example.com"}
    )
    user_id = create_response.json()["User"]["id"]
    
    # Agora, atualize o usuário
    response = client.put(
        f"/api/users/{user_id}",
        json={"first_name": "Updated", "email": "updated@example.com"}
    )
    assert response.status_code == 200
    assert response.json()["User"]["first_name"] == "Updated"
    assert response.json()["User"]["email"] == "updated@example.com"

def test_delete_user():
    # Primeiro, crie um usuário
    create_response = client.post(
        "/api/users/",
        json={"first_name": "Delete", "last_name": "Test", "email": "delete@example.com"}
    )
    user_id = create_response.json()["User"]["id"]
    
    # Agora, delete o usuário
    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 200
    
    # Verifique se o usuário foi realmente deletado
    get_response = client.get(f"/api/users/{user_id}")
    assert get_response.status_code == 404

def test_list_users():
    response = client.get("/api/users/")
    assert response.status_code == 200
    assert "users" in response.json()
