from sqlalchemy.orm import Session
from app.repository.party import PartyRepository
from app.models import Party
from app.schemas import PartyCreate
from fastapi import HTTPException
from app.interfaces.concrete.transaction_concrete import TransactionConcrete


class PartyService:
    def __init__(self, db: Session, transaction_concrete: TransactionConcrete):
        self.repository = PartyRepository(db)
        self.transaction_concrete = transaction_concrete

    def add_party_service(self, party_data: PartyCreate) -> Party:
        try:
            # A validação do cpf/cnpj acontece automaticamente pelo Pydantic
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

        except HTTPException as e:
            # Já é tratado pelo validator
            raise e
        except Exception as e:
            print("Erro interno:", e)
            raise HTTPException(status_code=500, detail="intern wrong")

    def remove_party(self, party_id: str):
        party = self.repository.get_party_by_id(party_id)
        if not party:
            raise HTTPException(404, "Party not found")
        
        transaction = self.transaction_concrete.get_transaction_service(party.transaction_id_fk)
        
        if transaction.status == "APPROVED":
            raise HTTPException(400, "Cannot delete party linked to an APPROVED transaction")
        
        self.repository.delete(party)
