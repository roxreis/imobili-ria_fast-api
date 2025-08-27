from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr
from app.models import TransactionStatus


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
    transaction_id: UUID | str


class Party(PartyBase):
    party_id: UUID | str
    transaction_id: UUID | str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PartyOut(PartyBase):
    party_id: UUID | str

    class Config:
        orm_mode = True


class CommissionCreate(BaseModel):
    percentage: Decimal 
    transaction_id: UUID | str


class CommissionOut(BaseModel):
    commission_id: UUID | str
    percentage: Decimal
    transaction_id_fk: UUID | str
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
    transaction_id: UUID | str
    status: TransactionStatus
    created_at: datetime
    updated_at: datetime
    parties: List[PartyOut] = []
    commissions: List[CommissionOut] = []

    class Config:
        orm_mode = True


class StatusUpdate(BaseModel):
    new_status: TransactionStatus
