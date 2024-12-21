"""
Módulo de Endpoints de Conta

Este módulo contém todas as rotas relacionadas às operações de conta,
incluindo CRUD e gerenciamento de contas.

Autor: Wilson Ferreira Junior
Data: 20 de Dezembro de 2024
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.models import Account, User
from app.core.auth import get_current_user
from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime, timezone

router = APIRouter()

class AccountCreate(BaseModel):
    """Modelo para criação de conta."""
    account_name: str
    balance: Decimal
    account_type: str

class AccountUpdate(BaseModel):
    """Modelo para atualização de conta com campos opcionais."""
    account_name: str = None
    balance: Decimal = None
    account_type: str = None

class AccountOut(BaseModel):
    """
    Modelo para retorno de dados da conta.
    """
    id: int
    user_id: int
    account_name: str
    balance: Decimal
    account_type: str

    model_config = ConfigDict(from_attributes=True)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AccountOut)
def create_account(
    account: AccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> AccountOut:
    """
    Cria uma nova conta para o usuário autenticado.

    Args:
        account: Dados da conta a ser criada
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        AccountOut: Dados da conta criada
    """
    db_account = Account(
        user_id=current_user.id,
        account_name=account.account_name,
        balance=account.balance,
        account_type=account.account_type
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@router.get("/", response_model=list[AccountOut])
def read_accounts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> list[AccountOut]:
    """
    Lista todas as contas do usuário autenticado com paginação.

    Args:
        skip: Número de registros para pular
        limit: Número máximo de registros a retornar
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        list[AccountOut]: Lista de contas do usuário
    """
    accounts = db.query(Account).filter(Account.user_id == current_user.id).offset(skip).limit(limit).all()
    return accounts

@router.get("/{account_id}", response_model=AccountOut)
def read_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> AccountOut:
    """
    Retorna os dados de uma conta específica do usuário autenticado.

    Args:
        account_id: ID da conta
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        AccountOut: Dados da conta solicitada

    Raises:
        HTTPException: Quando a conta não é encontrada ou não pertence ao usuário
    """
    account = db.query(Account).filter(Account.id == account_id, Account.user_id == current_user.id).first()
    if account is None:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return account

@router.put("/{account_id}", response_model=AccountOut)
def update_account(
    account_id: int,
    account: AccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> AccountOut:
    """
    Atualiza os dados de uma conta do usuário autenticado.

    Args:
        account_id: ID da conta a ser atualizada
        account: Novos dados da conta
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        AccountOut: Dados atualizados da conta

    Raises:
        HTTPException: Quando a conta não é encontrada ou não pertence ao usuário
    """
    db_account = db.query(Account).filter(Account.id == account_id, Account.user_id == current_user.id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    update_data = account.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_account, key, value)
    
    db.commit()
    db.refresh(db_account)
    return db_account

@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Response:
    """
    Remove uma conta do usuário autenticado.

    Args:
        account_id: ID da conta a ser removida
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Response: Resposta vazia com status 204

    Raises:
        HTTPException: Quando a conta não é encontrada ou não pertence ao usuário
    """
    db_account = db.query(Account).filter(Account.id == account_id, Account.user_id == current_user.id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    db.delete(db_account)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
