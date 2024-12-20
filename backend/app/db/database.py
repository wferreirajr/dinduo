from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base  # Atualizado

SQLALCHEMY_DATABASE_URL = "sqlite:///./dinduo.sqlite"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # Esta linha permanece a mesma

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
