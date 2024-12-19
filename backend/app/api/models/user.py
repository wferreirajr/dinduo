from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL, Date
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    account_name = Column(String, nullable=False)
    balance = Column(DECIMAL(10, 2), nullable=False, default=0)
    account_type = Column(String, nullable=False)
    user = relationship("User")

class Card(Base):
    __tablename__ = "cards"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    card_name = Column(String, nullable=False)
    limit = Column(DECIMAL(10, 2), nullable=False)
    closing_day = Column(Integer, nullable=False)
    due_day = Column(Integer, nullable=False)
    user = relationship("User")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    user = relationship("User")

class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    card_id = Column(Integer, ForeignKey('cards.id'))
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String)
    user = relationship("User")
    account = relationship("Account")
    card = relationship("Card")
    category = relationship("Category")