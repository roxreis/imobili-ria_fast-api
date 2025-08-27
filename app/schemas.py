from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr
from app.models import TransactionStatus
from app.validators import validate_cpf_cnpj, get_cpf_cnpj_type 


class PartyType(str, Enum):
    BUYER = "BUYER"
    SELLER = "SELLER"
    BROKER = "BROKER"


class PartyBase(BaseModel):
    type: PartyType
    name: str
    cpf_cnpj: str
    email: Optional[EmailStr] = None

    @field_validator('cpf_cnpj')
    @classmethod
    def validate_and_format_cpf_cnpj(cls, v):
        return validate_cpf_cnpj(v)

    @field_validator('document_type', mode='before', check_fields=False)
    @classmethod
    def set_document_type(cls, v, values):
        if 'cpf_cnpj' in values.data:
            return get_cpf_cnpj_type(values.data['cpf_cnpj'])
        return v


class PartyCreate(PartyBase):
    transaction_id: UUID | str
    type: PartyType
    cpf_cnpj: str
    email: Optional[EmailStr] = None


class Party(PartyBase):
    party_id: UUID | str
    transaction_id: UUID | str
    type: PartyType
    cpf_cnpj: str
    email: Optional[EmailStr] = None
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
