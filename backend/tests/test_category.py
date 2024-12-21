import pytest

@pytest.fixture
def test_category(authorized_client):
    category_data = {
        "category_name": "Test Category",
        "type": "Expense"
    }
    response = authorized_client.post("/api/v1/categories/", json=category_data)
    assert response.status_code == 201
    return response.json()

def test_create_category(authorized_client):
    category_data = {
        "category_name": "New Test Category",
        "type": "Income"
    }
    response = authorized_client.post("/api/v1/categories/", json=category_data)
    assert response.status_code == 201
    data = response.json()
    assert data["category_name"] == "New Test Category"
    assert data["type"] == "Income"
    assert "id" in data

def test_read_categories(authorized_client, test_category):
    response = authorized_client.get("/api/v1/categories/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_read_category(authorized_client, test_category):
    response = authorized_client.get(f"/api/v1/categories/{test_category['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["category_name"] == test_category["category_name"]
    assert data["type"] == test_category["type"]

def test_update_category(authorized_client, test_category):
    update_data = {
        "category_name": "Updated Category",
        "type": "Transfer"
    }
    response = authorized_client.put(
        f"/api/v1/categories/{test_category['id']}",
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["category_name"] == update_data["category_name"]
    assert data["type"] == update_data["type"]

def test_delete_category(authorized_client, test_category):
    response = authorized_client.delete(f"/api/v1/categories/{test_category['id']}")
    assert response.status_code == 204
    
    get_response = authorized_client.get(f"/api/v1/categories/{test_category['id']}")
    assert get_response.status_code == 404
