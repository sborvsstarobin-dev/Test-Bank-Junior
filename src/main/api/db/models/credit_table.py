from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from src.main.api.db.base import Base


class Credit(Base):
    __tablename__ = 'credit'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    amount = Column(Float, unique=False)
    term_months = Column(Integer, unique=False)
    balance = Column(Float, unique=True)
    created_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Credit(id={self.id}, account_id={self.account_id}, amount={self.amount}, term_month={self.term_month}, balance={self.balance}, created_at={self.created_at})>"
