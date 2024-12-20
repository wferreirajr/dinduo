"""
Módulo de Autenticação

Este módulo gerencia a autenticação JWT (JSON Web Token) da aplicação,
incluindo a criação de tokens e validação de usuários.

Autor: Wilson Ferreira Junior
Data: 20 de Dezembro de 2024
"""

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import verify_password
from app.api.models.user import User
from app.db.database import get_db


# Configuração do esquema OAuth2 com o endpoint correto para obtenção do token
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/users/token"
)


def create_access_token(data: dict) -> str:
    """
    Cria um token JWT com os dados fornecidos.

    Args:
        data (dict): Dicionário contendo os dados a serem codificados no token

    Returns:
        str: Token JWT codificado
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Obtém o usuário atual baseado no token JWT.

    Args:
        token (str): Token JWT fornecido no header de autorização
        db (Session): Sessão do banco de dados

    Returns:
        User: Instância do usuário autenticado

    Raises:
        HTTPException: Quando as credenciais não podem ser validadas
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodifica o token JWT
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        
        # Extrai o email do payload
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Busca o usuário no banco de dados
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user
