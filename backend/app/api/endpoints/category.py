"""
Módulo de Endpoints de Categoria

Este módulo contém todas as rotas relacionadas às operações de categoria,
incluindo CRUD e gerenciamento de categorias.

Autor: Wilson Ferreira Junior
Data: 20 de Dezembro de 2024
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.models import Category, User
from app.core.auth import get_current_user
from pydantic import BaseModel, ConfigDict
from datetime import datetime, timezone

router = APIRouter()

class CategoryCreate(BaseModel):
    """Modelo para criação de categoria."""
    category_name: str
    type: str

class CategoryUpdate(BaseModel):
    """Modelo para atualização de categoria com campos opcionais."""
    category_name: str = None
    type: str = None

class CategoryOut(BaseModel):
    """
    Modelo para retorno de dados da categoria.
    """
    id: int
    user_id: int
    category_name: str
    type: str

    model_config = ConfigDict(from_attributes=True)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CategoryOut)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> CategoryOut:
    """
    Cria uma nova categoria para o usuário autenticado.

    Args:
        category: Dados da categoria a ser criada
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        CategoryOut: Dados da categoria criada
    """
    db_category = Category(
        user_id=current_user.id,
        category_name=category.category_name,
        type=category.type
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/", response_model=list[CategoryOut])
def read_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> list[CategoryOut]:
    """
    Lista todas as categorias do usuário autenticado com paginação.

    Args:
        skip: Número de registros para pular
        limit: Número máximo de registros a retornar
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        list[CategoryOut]: Lista de categorias do usuário
    """
    categories = db.query(Category).filter(Category.user_id == current_user.id).offset(skip).limit(limit).all()
    return categories

@router.get("/{category_id}", response_model=CategoryOut)
def read_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> CategoryOut:
    """
    Retorna os dados de uma categoria específica do usuário autenticado.

    Args:
        category_id: ID da categoria
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        CategoryOut: Dados da categoria solicitada

    Raises:
        HTTPException: Quando a categoria não é encontrada ou não pertence ao usuário
    """
    category = db.query(Category).filter(Category.id == category_id, Category.user_id == current_user.id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return category

@router.put("/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> CategoryOut:
    """
    Atualiza os dados de uma categoria do usuário autenticado.

    Args:
        category_id: ID da categoria a ser atualizada
        category: Novos dados da categoria
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        CategoryOut: Dados atualizados da categoria

    Raises:
        HTTPException: Quando a categoria não é encontrada ou não pertence ao usuário
    """
    db_category = db.query(Category).filter(Category.id == category_id, Category.user_id == current_user.id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    update_data = category.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Response:
    """
    Remove uma categoria do usuário autenticado.

    Args:
        category_id: ID da categoria a ser removida
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Response: Resposta vazia com status 204

    Raises:
        HTTPException: Quando a categoria não é encontrada ou não pertence ao usuário
    """
    db_category = db.query(Category).filter(Category.id == category_id, Category.user_id == current_user.id).first()
    if db_category is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    db.delete(db_category)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
