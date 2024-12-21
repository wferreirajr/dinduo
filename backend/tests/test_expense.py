import pytest
from decimal import Decimal
from datetime import date

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

@pytest.fixture
def test_category(authorized_client):
    category_data = {
        "category_name": "Test Category",
        "type": "Expense"
    }
    response = authorized_client.post("/api/v1/categories/", json=category_data)
    assert response.status_code == 201
    return response.json()

@pytest.fixture
def test_expense(authorized_client, test_account, test_card, test_category):
    expense_data = {
        "account_id": test_account["id"],
        "card_id": test_card["id"],
        "category_id": test_category["id"],
        "amount": 100.00,
        "date": str(date.today()),
        "description": "Test Expense"
    }
    response = authorized_client.post("/api/v1/expenses/", json=expense_data)
    assert response.status_code == 201
    return response.json()

@pytest.mark.run(order=5)
def test_create_expense(authorized_client, test_account, test_card, test_category):
    expense_data = {
        "account_id": test_account["id"],
        "card_id": test_card["id"],
        "category_id": test_category["id"],
        "amount": 50.00,
        "date": str(date.today()),
        "description": "New Test Expense"
    }
    response = authorized_client.post("/api/v1/expenses/", json=expense_data)
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == "50.00"
    assert data["description"] == "New Test Expense"
    assert "id" in data

@pytest.mark.run(order=6)
def test_read_expenses(authorized_client, test_expense):
    response = authorized_client.get("/api/v1/expenses/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

@pytest.mark.run(order=7)
def test_read_expense(authorized_client, test_expense):
    response = authorized_client.get(f"/api/v1/expenses/{test_expense['id']}")
    assert response.status_code == 200
    data = response.json()
    assert Decimal(data["amount"]) == Decimal(test_expense["amount"])
    assert data["description"] == test_expense["description"]

@pytest.mark.run(order=8)
def test_update_expense(authorized_client, test_expense):
    update_data = {
        "amount": 75.00,
        "description": "Updated Expense"
    }
    response = authorized_client.put(
        f"/api/v1/expenses/{test_expense['id']}",
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert Decimal(data["amount"]) == Decimal("75.00")
    assert data["description"] == "Updated Expense"

@pytest.mark.run(order=9)
def test_delete_expense(authorized_client, test_expense):
    response = authorized_client.delete(f"/api/v1/expenses/{test_expense['id']}")
    assert response.status_code == 204
    
    get_response = authorized_client.get(f"/api/v1/expenses/{test_expense['id']}")
    assert get_response.status_code == 404

def test_get_expense_summary(authorized_client, test_expense):
    response = authorized_client.get("/api/v1/expenses/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_amount" in data
    assert "expense_count" in data
    assert "category_summary" in data
