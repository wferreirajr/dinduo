# Arquivo: main.py
from fastapi import FastAPI
from app.api.endpoints import user, account
from app.core.config import settings
from app.db.database import engine, Base

# Inicialização do banco de dados
Base.metadata.create_all(bind=engine)

# Criação da aplicação FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para gerenciamento de usuários e contas",
    version="1.0.0"
)

# Inclusão dos roteadores
app.include_router(user.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(account.router, prefix=f"{settings.API_V1_STR}/accounts", tags=["accounts"])

# Rota raiz
@app.get("/")
async def root():
    return {"message": "Bem-vindo à API"}
