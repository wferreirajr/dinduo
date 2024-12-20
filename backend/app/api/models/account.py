from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from app.db.database import Base

class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    account_name = Column(String(100), nullable=False)
    balance = Column(DECIMAL(10, 2), nullable=False, default=0)
    account_type = Column(String(50), nullable=False)

    user = relationship("User", back_populates="accounts")
    expenses = relationship("Expense", back_populates="account", cascade="all, delete-orphan")
