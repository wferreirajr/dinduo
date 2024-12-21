import pytest
from decimal import Decimal

@pytest.fixture
def test_account(authorized_client):
    account_data = {
        "account_name": "Test Account",
        "balance": 1000.00,
        "account_type": "Savings"
    }
    response = authorized_client.post("/api/v1/accounts/", json=account_data)
    assert response.status_code == 201
    return response.json()

def test_create_account(authorized_client):
    account_data = {
        "account_name": "New Test Account",
        "balance": 500.00,
        "account_type": "Checking"
    }
    response = authorized_client.post("/api/v1/accounts/", json=account_data)
    assert response.status_code == 201
    data = response.json()
    assert data["account_name"] == "New Test Account"
    assert Decimal(data["balance"]) == Decimal("500.00")
    assert data["account_type"] == "Checking"
    assert "id" in data

def test_read_accounts(authorized_client, test_account):
    response = authorized_client.get("/api/v1/accounts/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_read_account(authorized_client, test_account):
    response = authorized_client.get(f"/api/v1/accounts/{test_account['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["account_name"] == test_account["account_name"]
    assert Decimal(data["balance"]) == Decimal(test_account["balance"])
    assert data["account_type"] == test_account["account_type"]

def test_update_account(authorized_client, test_account):
    update_data = {
        "account_name": "Updated Account",
        "balance": 1500.00,
        "account_type": "Investment"
    }
    response = authorized_client.put(
        f"/api/v1/accounts/{test_account['id']}",
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["account_name"] == update_data["account_name"]
    assert Decimal(data["balance"]) == Decimal(update_data["balance"])
    assert data["account_type"] == update_data["account_type"]

def test_delete_account(authorized_client, test_account):
    response = authorized_client.delete(f"/api/v1/accounts/{test_account['id']}")
    assert response.status_code == 204
    
    get_response = authorized_client.get(f"/api/v1/accounts/{test_account['id']}")
    assert get_response.status_code == 404
