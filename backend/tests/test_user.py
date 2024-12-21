import pytest
from app.api.models import User
from conftest import get_unique_email

def test_create_user(client):
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
    response = authorized_client.delete(f"/api/v1/users/{test_user['user']['id']}")
    assert response.status_code == 204

    get_response = authorized_client.get(f"/api/v1/users/{test_user['user']['id']}")
    assert get_response.status_code == 404
"""
