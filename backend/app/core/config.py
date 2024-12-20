"""
Módulo de Configuração

Este módulo gerencia todas as configurações para a aplicação FastAPI,
incluindo conexões de banco de dados, configurações JWT e versionamento da API.

Autor: [Seu Nome]
Data: [Data Atual]
"""

import os
from secrets import token_hex
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configurações e variáveis de ambiente da aplicação.

    Esta classe utiliza o BaseSettings do Pydantic para gerenciar todas as variáveis de configuração,
    suportando tanto variáveis de ambiente quanto carregamento de arquivo .env.

    Atributos:
        PROJECT_NAME (str): Nome do projeto
        API_V1_STR (str): Prefixo da versão da API para todos os endpoints
        DATABASE_URL (str): URL de conexão do banco de dados SQLite
        SECRET_KEY (str): Chave secreta para geração e validação de tokens JWT
        ALGORITHM (str): Algoritmo usado para criptografia do token JWT
        ACCESS_TOKEN_EXPIRE_MINUTES (int): Tempo de expiração do token JWT em minutos
    """

    PROJECT_NAME: str = "FastAPI CRUD"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./dinduo.sqlite"
    SECRET_KEY: str = os.getenv("SECRET_KEY", token_hex(32))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        """Configuração do Pydantic."""
        env_file = ".env"
        case_sensitive = True


# Inicializa a instância de configurações
settings = Settings()
