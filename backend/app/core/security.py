"""
Módulo de Segurança

Este módulo fornece funções para hash e verificação de senhas usando bcrypt.
Implementa as melhores práticas de segurança para armazenamento seguro de senhas.

Autor: Wilson Ferreira Junior
Data: 20 de Dezembro de 2024
"""

from passlib.context import CryptContext


# Configuração do contexto de criptografia
# Utiliza bcrypt como algoritmo principal de hash
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def get_password_hash(password: str) -> str:
    """
    Gera um hash seguro para a senha fornecida.

    Args:
        password (str): Senha em texto plano a ser hasheada

    Returns:
        str: Hash da senha usando bcrypt

    Exemplo:
        >>> hash = get_password_hash("minha_senha")
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde ao hash armazenado.

    Args:
        plain_password (str): Senha em texto plano a ser verificada
        hashed_password (str): Hash da senha armazenado

    Returns:
        bool: True se a senha corresponde ao hash, False caso contrário

    Exemplo:
        >>> is_valid = verify_password("minha_senha", hash_armazenado)
    """
    return pwd_context.verify(plain_password, hashed_password)
