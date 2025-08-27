from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import Party


class PartyRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_party(self, party: Party):
        self.db.add(party)
        self.db.commit()
        self.db.refresh(party)
        return party

    def get_party_by_id(self, party_id: str):
        return self.db.query(Party).filter_by(party_id=party_id).first()

    def delete(self, party: Party):
        self.db.delete(party)
        self.db.commit()
        
    def find_party_by_cpf_or_email(self, cpf_cnpj: str, email: str) -> Optional[Party]:
        return self.db.query(Party).filter(
            or_(Party.cpf_cnpj == cpf_cnpj, Party.email == email)
        ).first()
