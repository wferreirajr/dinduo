from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Date
from sqlalchemy.orm import relationship
from app.db.database import Base

class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    card_id = Column(Integer, ForeignKey('cards.id'))
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    date = Column(Date, nullable=False, index=True)
    description = Column(String(255))

    user = relationship("User", back_populates="expenses")
    account = relationship("Account", back_populates="expenses")
    card = relationship("Card", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")
