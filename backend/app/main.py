"""
FastAPI Main Application Module

This module initializes and configures the FastAPI application, including database setup,
route registration, and authentication middleware.

Author: Wilson Ferreira Junior
Date: December 20, 2024
"""

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from app.api.endpoints import user, account
from app.core.config import settings
from app.db.database import engine, Base
from app.core.auth import get_current_user


def init_database() -> None:
    """Initialize database by creating all defined tables."""
    Base.metadata.create_all(bind=engine)


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="API para gerenciamento de usuários e contas",
        version="1.0.0",
    )

    # Register routers with their respective prefixes and tags
    app.include_router(
        user.router,
        prefix=f"{settings.API_V1_STR}/users",
        tags=["users"],
    )
    app.include_router(
        account.router,
        prefix=f"{settings.API_V1_STR}/accounts",
        tags=["accounts"],
    )

    return app


# Initialize database
init_database()

# Create FastAPI application instance
app = create_application()


@app.get("/")
async def root() -> dict:
    """
    Root endpoint that provides a welcome message.

    Returns:
        dict: Welcome message
    """
    return {"message": "Bem-vindo à API"}


@app.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Protected route example that requires authentication.

    Args:
        current_user (dict): Current authenticated user, injected by dependency

    Returns:
        dict: Personalized message for authenticated user
    """
    return {
        "message": f"Olá, {current_user.name}! Esta é uma rota protegida."
    }
