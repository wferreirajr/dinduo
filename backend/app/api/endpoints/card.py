"""
Módulo de Endpoints de Cartão

Este módulo contém todas as rotas relacionadas às operações de cartão,
incluindo CRUD e gerenciamento de cartões.

Autor: Wilson Ferreira Junior
Data: 20 de Dezembro de 2024
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.models import Card, User
from app.core.auth import get_current_user
from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from datetime import datetime, timezone

router = APIRouter()

class CardCreate(BaseModel):
    """Modelo para criação de cartão."""
    card_name: str
    limit: Decimal
    closing_day: int
    due_day: int

class CardUpdate(BaseModel):
    """Modelo para atualização de cartão com campos opcionais."""
    card_name: str = None
    limit: Decimal = None
    closing_day: int = None
    due_day: int = None

class CardOut(BaseModel):
    """
    Modelo para retorno de dados do cartão.
    """
    id: int
    user_id: int
    card_name: str
    limit: Decimal
    closing_day: int
    due_day: int

    model_config = ConfigDict(from_attributes=True)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CardOut)
def create_card(
    card: CardCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> CardOut:
    """
    Cria um novo cartão para o usuário autenticado.

    Args:
        card: Dados do cartão a ser criado
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        CardOut: Dados do cartão criado
    """
    db_card = Card(
        user_id=current_user.id,
        card_name=card.card_name,
        limit=card.limit,
        closing_day=card.closing_day,
        due_day=card.due_day
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

@router.get("/", response_model=list[CardOut])
def read_cards(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> list[CardOut]:
    """
    Lista todos os cartões do usuário autenticado com paginação.

    Args:
        skip: Número de registros para pular
        limit: Número máximo de registros a retornar
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        list[CardOut]: Lista de cartões do usuário
    """
    cards = db.query(Card).filter(Card.user_id == current_user.id).offset(skip).limit(limit).all()
    return cards

@router.get("/{card_id}", response_model=CardOut)
def read_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> CardOut:
    """
    Retorna os dados de um cartão específico do usuário autenticado.

    Args:
        card_id: ID do cartão
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        CardOut: Dados do cartão solicitado

    Raises:
        HTTPException: Quando o cartão não é encontrado ou não pertence ao usuário
    """
    card = db.query(Card).filter(Card.id == card_id, Card.user_id == current_user.id).first()
    if card is None:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    return card

@router.put("/{card_id}", response_model=CardOut)
def update_card(
    card_id: int,
    card: CardUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> CardOut:
    """
    Atualiza os dados de um cartão do usuário autenticado.

    Args:
        card_id: ID do cartão a ser atualizado
        card: Novos dados do cartão
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        CardOut: Dados atualizados do cartão

    Raises:
        HTTPException: Quando o cartão não é encontrado ou não pertence ao usuário
    """
    db_card = db.query(Card).filter(Card.id == card_id, Card.user_id == current_user.id).first()
    if db_card is None:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    
    update_data = card.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_card, key, value)
    
    db.commit()
    db.refresh(db_card)
    return db_card

@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(
    card_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Response:
    """
    Remove um cartão do usuário autenticado.

    Args:
        card_id: ID do cartão a ser removido
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Response: Resposta vazia com status 204

    Raises:
        HTTPException: Quando o cartão não é encontrado ou não pertence ao usuário
    """
    db_card = db.query(Card).filter(Card.id == card_id, Card.user_id == current_user.id).first()
    if db_card is None:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    
    db.delete(db_card)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
