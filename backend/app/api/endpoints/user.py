"""
Módulo de Endpoints de Usuário

Este módulo contém todas as rotas relacionadas às operações de usuário,
incluindo autenticação, CRUD e gerenciamento de perfil.

Autor: Wilson Ferreira Junior
Data: 20 de Dezembro de 2024
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.models import User
from app.core.security import get_password_hash, verify_password
from app.core.auth import create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, ConfigDict
from datetime import datetime, timezone


router = APIRouter()

class UserCreate(BaseModel):
    """Modelo para criação de usuário."""
    name: str
    email: str
    password: str


class UserUpdate(BaseModel):
    """Modelo para atualização de usuário com campos opcionais."""
    name: str = None
    email: str = None
    password: str = None


class Token(BaseModel):
    """Modelo para token de autenticação."""
    access_token: str
    token_type: str


class UserOut(BaseModel):
    """
    Modelo para retorno de dados do usuário.
    
    Exclui informações sensíveis como senha.
    """
    id: int
    name: str
    email: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Token:
    """
    Autentica o usuário e retorna um token de acesso.

    Args:
        form_data: Dados do formulário de login
        db: Sessão do banco de dados

    Returns:
        Token: Token de acesso JWT

    Raises:
        HTTPException: Quando as credenciais são inválidas
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserOut:
    """
    Cria um novo usuário.

    Args:
        user: Dados do usuário a ser criado
        db: Sessão do banco de dados

    Returns:
        UserOut: Dados do usuário criado
    """
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        created_at=datetime.now(timezone.utc)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=list[UserOut])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> list[UserOut]:
    """
    Lista todos os usuários com paginação.

    Args:
        skip: Número de registros para pular
        limit: Número máximo de registros a retornar
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        list[UserOut]: Lista de usuários
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)) -> UserOut:
    """
    Retorna os dados do usuário autenticado.

    Args:
        current_user: Usuário autenticado atual

    Returns:
        UserOut: Dados do usuário atual
    """
    return current_user


@router.get("/{user_id}", response_model=UserOut)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> UserOut:
    """
    Retorna os dados de um usuário específico.

    Args:
        user_id: ID do usuário
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        UserOut: Dados do usuário solicitado

    Raises:
        HTTPException: Quando o usuário não é encontrado
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> UserOut:
    """
    Atualiza os dados de um usuário.

    Args:
        user_id: ID do usuário a ser atualizado
        user: Novos dados do usuário
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        UserOut: Dados atualizados do usuário

    Raises:
        HTTPException: Quando o usuário não é encontrado
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    update_data = user.model_dump(exclude_unset=True)
    if 'password' in update_data:
        update_data['hashed_password'] = get_password_hash(
            update_data.pop('password')
        )
    
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Response:
    """
    Remove um usuário do sistema.

    Args:
        user_id: ID do usuário a ser removido
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        Response: Resposta vazia com status 204

    Raises:
        HTTPException: Quando o usuário não é encontrado
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    db.delete(db_user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
