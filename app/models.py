import uuid
import enum
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class TransactionStatus(str, enum.Enum):
    CREATED = "CREATED"
    UNDER_ANALYSIS = "UNDER_ANALYSIS"  
    APPROVED = "APPROVED"
    COMPLETED = "COMPLETED"  
    CANCELLED = "CANCELLED"

class PartyType(str, enum.Enum):
    BUYER = "BUYER"
    SELLER = "SELLER"
    BROKER = "BROKER"
    
class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    property_code = Column(String, nullable=False)
    sale_value = Column(Numeric(12, 2), nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.CREATED, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    parties = relationship("Party", back_populates="transaction", cascade="all, delete-orphan")
    commissions = relationship("Commission", back_populates="transaction", cascade="all, delete-orphan")

class Party(Base):
    __tablename__ = "parties"

    party_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    transaction_id_fk = Column(String, ForeignKey("transactions.transaction_id"), nullable=False)
    type = Column(Enum(PartyType), nullable=False)
    name = Column(String, nullable=False)
    cpf_cnpj = Column(String, nullable=False)
    email = Column(String, nullable=True)

    transaction = relationship("Transaction", back_populates="parties")

class Commission(Base):
    __tablename__ = "commissions"

    commission_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    transaction_id_fk = Column(String, ForeignKey("transactions.transaction_id"), nullable=False)
    percentage = Column(Numeric(5, 4), nullable=False)
    calculated_amount = Column(Numeric(12, 2), nullable=False)
    paid = Column(Boolean, default=False)

    transaction = relationship("Transaction", back_populates="commissions")
