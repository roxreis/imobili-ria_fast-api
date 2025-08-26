from sqlalchemy.orm import Session
from app.repository.party import PartyRepository
from app.models import Party
from app.schemas import PartyCreate
from fastapi import HTTPException
import re


def validate_cpf(cpf: str) -> bool:
    cpf = re.sub(r'[^0-9]', '', cpf)

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    sum1 = 0
    for i in range(9):
        sum1 += int(cpf[i]) * (10 - i)

    remainder1 = sum1 % 11
    digit1 = 0 if remainder1 < 2 else 11 - remainder1

    if int(cpf[9]) != digit1:
        return False

    sum2 = 0
    for i in range(10):
        sum2 += int(cpf[i]) * (11 - i)

    remainder2 = sum2 % 11
    digit2 = 0 if remainder2 < 2 else 11 - remainder2

    if int(cpf[10]) != digit2:
        return False

    return True


def validate(value: str) -> None:
    if not validate_cpf(value):
        raise ValueError('CPF inválido')

def is_buyer_validate(value: str):
    if value.lower() == 'buyer':
        raise ValueError('O tipo de party não pode ser comprador')


class PartyService:
    def __init__(self, db: Session):
        self.repository = PartyRepository(db)

    def add_party_service(self, party_data: PartyCreate) -> Party:
        validate(party_data.cpf_cnpj)
        is_buyer_validate(party_data.type)

        existing_party = self.repository.find_party_by_cpf_or_email(
            cpf_cnpj=party_data.cpf_cnpj,
            email=party_data.email  
        )

        if existing_party:
            if existing_party.cpf_cnpj == party_data.cpf_cnpj:
                raise HTTPException(
                    status_code=400,
                    detail="A party with this CPF/CNPJ already exists."
                )
            if existing_party.email == party_data.email:
                raise HTTPException(
                    status_code=400,
                    detail="A party with this email already exists."
                )
        
        party_dict = party_data.dict()
        party_dict['transaction_id_fk'] = party_dict.pop('transaction_id', None)
        
        party = Party(**party_dict)
        return self.repository.create_party(party)

    def remove_party(self, party_id: str):
        party = self.repository.get_by_id(party_id)
        if not party:
            raise HTTPException(404, "Party not found")
        self.repository.delete(party)
