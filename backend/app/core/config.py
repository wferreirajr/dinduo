from pydantic_settings import BaseSettings
from secrets import token_hex
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI CRUD"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    SECRET_KEY: str = os.getenv("SECRET_KEY", token_hex(32))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()
