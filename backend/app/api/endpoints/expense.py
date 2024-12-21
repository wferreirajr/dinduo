"""
Módulo de Endpoints de Despesa

Este módulo contém todas as rotas relacionadas às operações de despesa,
incluindo CRUD e gerenciamento de despesas.

Autor: Wilson Ferreira Junior
Data: 20 de Dezembro de 2024
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.models import Expense, User
from app.core.auth import get_current_user
from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import date, datetime, timezone

router = APIRouter()

class ExpenseCreate(BaseModel):
    """Modelo para criação de despesa."""
    account_id: int = None
    card_id: int = None
    category_id: int
    amount: Decimal
    date: date
    description: str = None

class ExpenseUpdate(BaseModel):
    """Modelo para atualização de despesa com campos opcionais."""
    account_id: int = None
    card_id: int = None
    category_id: int = None
    amount: Decimal = None
    date: date = None
    description: str = None

class ExpenseOut(BaseModel):
    """
    Modelo para retorno de dados da despesa.
    """
    id: int
    user_id: int
    account_id: int = None
    card_id: int = None
    category_id: int
    amount: Decimal
    date: date
    description: str = None

    model_config = ConfigDict(from_attributes=True)

@router.get("/summary", response_model=dict)
def get_expense_summary(
    start_date: date = None,
    end_date: date = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    query = db.query(Expense).filter(Expense.user_id == current_user.id)
    
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)
    
    expenses = query.all()
    
    total_amount = sum(expense.amount for expense in expenses)
    expense_count = len(expenses)
    
    category_summary = {}
    detailed_expenses = []
    
    for expense in expenses:
        category = expense.category.category_name
        if category not in category_summary:
            category_summary[category] = 0
        category_summary[category] += expense.amount
        
        detailed_expenses.append({
            "id": expense.id,
            "amount": str(expense.amount),
            "date": expense.date.isoformat(),
            "description": expense.description,
            "category": category,
            "account_name": expense.account.account_name if expense.account else None,
            "card_name": expense.card.card_name if expense.card else None
        })
    
    return {
        "total_amount": str(total_amount),
        "expense_count": expense_count,
        "category_summary": {cat: str(amount) for cat, amount in category_summary.items()},
        "detailed_expenses": detailed_expenses
    }

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ExpenseOut)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ExpenseOut:
    """
    Cria uma nova despesa para o usuário autenticado.

    Args:
        expense: Dados da despesa a ser criada
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        ExpenseOut: Dados da despesa criada
    """
    db_expense = Expense(
        user_id=current_user.id,
        account_id=expense.account_id,
        card_id=expense.card_id,
        category_id=expense.category_id,
        amount=expense.amount,
        date=expense.date,
        description=expense.description
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.get("/", response_model=list[ExpenseOut])
def read_expenses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> list[ExpenseOut]:
    """
    Lista todas as despesas do usuário autenticado com paginação.

    Args:
        skip: Número de registros para pular
        limit: Número máximo de registros a retornar
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        list[ExpenseOut]: Lista de despesas do usuário
    """
    expenses = db.query(Expense).filter(Expense.user_id == current_user.id).offset(skip).limit(limit).all()
    return expenses

@router.get("/{expense_id}", response_model=ExpenseOut)
def read_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ExpenseOut:
    """
    Retorna os dados de uma despesa específica do usuário autenticado.

    Args:
        expense_id: ID da despesa
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        ExpenseOut: Dados da despesa solicitada

    Raises:
        HTTPException: Quando a despesa não é encontrada ou não pertence ao usuário
    """
    expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == current_user.id).first()
    if expense is None:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    return expense

@router.put("/{expense_id}", response_model=ExpenseOut)
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> ExpenseOut:
    """
    Atualiza os dados de uma despesa do usuário autenticado.

    Args:
        expense_id: ID da despesa a ser atualizada
        expense: Novos dados da despesa
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        ExpenseOut: Dados atualizados da despesa

    Raises:
        HTTPException: Quando a despesa não é encontrada ou não pertence ao usuário
    """
    db_expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == current_user.id).first()
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    
    update_data = expense.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_expense, key, value)
    
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Response:
    """
    Remove uma despesa do usuário autenticado.

    Args:
        expense_id: ID da despesa a ser removida
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Response: Resposta vazia com status 204

    Raises:
        HTTPException: Quando a despesa não é encontrada ou não pertence ao usuário
    """
    db_expense = db.query(Expense).filter(Expense.id == expense_id, Expense.user_id == current_user.id).first()
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Despesa não encontrada")
    
    db.delete(db_expense)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
