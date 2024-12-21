import pytest
from decimal import Decimal

@pytest.fixture
def test_card(authorized_client):
    card_data = {
        "card_name": "Test Card",
        "limit": 5000.00,
        "closing_day": 15,
        "due_day": 5
    }
    response = authorized_client.post("/api/v1/cards/", json=card_data)
    assert response.status_code == 201
    return response.json()

def test_create_card(authorized_client):
    card_data = {
        "card_name": "New Test Card",
        "limit": 3000.00,
        "closing_day": 20,
        "due_day": 10
    }
    response = authorized_client.post("/api/v1/cards/", json=card_data)
    assert response.status_code == 201
    data = response.json()
    assert data["card_name"] == "New Test Card"
    assert Decimal(data["limit"]) == Decimal("3000.00")
    assert data["closing_day"] == 20
    assert data["due_day"] == 10
    assert "id" in data

def test_read_cards(authorized_client, test_card):
    response = authorized_client.get("/api/v1/cards/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_read_card(authorized_client, test_card):
    response = authorized_client.get(f"/api/v1/cards/{test_card['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["card_name"] == test_card["card_name"]
    assert Decimal(data["limit"]) == Decimal(test_card["limit"])
    assert data["closing_day"] == test_card["closing_day"]
    assert data["due_day"] == test_card["due_day"]

def test_update_card(authorized_client, test_card):
    update_data = {
        "card_name": "Updated Card",
        "limit": 7500.00,
        "closing_day": 25,
        "due_day": 15
    }
    response = authorized_client.put(
        f"/api/v1/cards/{test_card['id']}",
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["card_name"] == update_data["card_name"]
    assert Decimal(data["limit"]) == Decimal(update_data["limit"])
    assert data["closing_day"] == update_data["closing_day"]
    assert data["due_day"] == update_data["due_day"]

def test_delete_card(authorized_client, test_card):
    response = authorized_client.delete(f"/api/v1/cards/{test_card['id']}")
    assert response.status_code == 204
    
    get_response = authorized_client.get(f"/api/v1/cards/{test_card['id']}")
    assert get_response.status_code == 404
