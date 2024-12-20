"""
Módulo de Configuração do Banco de Dados

Este módulo configura a conexão com o banco de dados SQLite e fornece
as classes e funções necessárias para interação com o banco de dados.

Autor: Wilson Ferreira Junior
Data: 20 de Dezembro de 2024
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings


# URL de conexão com o banco de dados
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Criação do engine do SQLAlchemy com configurações específicas para SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Necessário apenas para SQLite
)

# Configuração da sessão do banco de dados
SessionLocal = sessionmaker(
    autocommit=False,  # Desativa commit automático
    autoflush=False,   # Desativa flush automático
    bind=engine        # Vincula ao engine criado
)

# Classe base para os modelos SQLAlchemy
Base = declarative_base()


def get_db():
    """
    Gerador de contexto para gerenciar sessões do banco de dados.

    Yields:
        Session: Sessão do SQLAlchemy para interação com o banco de dados.

    Exemplo:
        db = next(get_db())
        try:
            # Operações no banco de dados
            db.commit()
        finally:
            db.close()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
