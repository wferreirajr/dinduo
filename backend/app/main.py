from fastapi import FastAPI
from app.api.endpoints import user
from app.core.config import settings
from app.db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(user.router, prefix=settings.API_V1_STR)
