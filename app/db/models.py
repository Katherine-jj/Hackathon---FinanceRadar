from sqlalchemy import Column, Integer, String, JSON, Boolean, DateTime, func, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Rule(Base):
    __tablename__ = "rules"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # "threshold", "pattern", "composite"
    params = Column(JSON, nullable=False)  # e.g. {"field":"amount","op":">","value":1000}
    enabled = Column(Boolean, default=True)

class TransactionLog(Base):
    __tablename__ = "transaction_logs"
    id = Column(Integer, primary_key=True)
    correlation_id = Column(String, index=True)
    payload = Column(JSON)
    alerted = Column(Boolean, default=False)
    alert_reason = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
