from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr
from app.models import TransactionStatus, PartyType


class PartyType(str, Enum):
    BUYER = "BUYER"
    SELLER = "SELLER"
    AGENT = "AGENT"
    BROKER = "BROKER"


class PartyBase(BaseModel):
    type: PartyType
    name: str
    cpf_cnpj: str 
    email: Optional[EmailStr] = None


class PartyCreate(PartyBase):
    transaction_id: UUID


class Party(PartyBase):
    party_id: UUID
    transaction_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PartyOut(PartyBase):
    party_id: UUID

    class Config:
        orm_mode = True


class CommissionCreate(BaseModel):
    percentage: Decimal = Field(..., gt=0, le=1)


class CommissionOut(BaseModel):
    commission_id: UUID
    percentage: Decimal
    calculated_amount: Decimal
    paid: bool

    class Config:
        orm_mode = True


class TransactionBase(BaseModel):
    property_code: str
    sale_value: Decimal


class TransactionCreate(TransactionBase):
    pass


class TransactionOut(TransactionBase):
    transaction_id: UUID
    status: TransactionStatus
    created_at: datetime
    updated_at: datetime
    parties: List[PartyOut] = []
    commissions: List[CommissionOut] = []

    class Config:
        orm_mode = True


class StatusUpdate(BaseModel):
    new_status: TransactionStatus
