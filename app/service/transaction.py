from __future__ import annotations

from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.repository.transaction import TransactionRepository
from app.models import Transaction
from app.database import get_db
from app.schemas import TransactionCreate, TransactionBase, PartyType
from app.interfaces.abstract.transaction_interface import TransactionInterface
from app.interfaces.concrete.transaction_concrete import TransactionConcrete


def get_concrete_transaction_service(
        db=Depends(get_db)
) -> TransactionInterface:
    return TransactionConcrete(db)


class TransactionService:
    def __init__(self, db: Session):
        self.repository = TransactionRepository(db)

    def create_transaction_service(self, transaction_data: TransactionCreate) -> Transaction:
        if not transaction_data.sale_value or transaction_data.sale_value <= 0:
            raise HTTPException(400, "Sale value must be greater than zero")
        if not transaction_data.property_code:
            raise HTTPException(400, "Property code is required")
        
        transaction = Transaction(
            property_code=transaction_data.property_code,
            sale_value=transaction_data.sale_value,  
            status="CREATED"
        )
        return self.repository.create_transaction(transaction)

    def get_transaction_service(self, transaction_id: UUID | str) -> Transaction:
        transaction = self.repository.get_transaction_by_id(transaction_id)
        if not transaction:
            raise HTTPException(404, "Transaction not found")
        return transaction

    def list_transactions_service(
            self,
            filters: dict,
            limit: int = 10, 
            offset: int = 0
    ):
        return self.repository.list_transactions_repository(filters, limit, offset)

    def update_transaction(self, transaction_id: str, transaction_data: TransactionBase):
        transaction = self.get_transaction_service(transaction_id)
        for key, value in transaction_data.dict().items():
            setattr(transaction, key, value)
            
        return self.repository.update_transaction(transaction)

    def delete_transaction(self, transaction_id: str):
        transaction = self.get_transaction_service(transaction_id)
        self.repository.delete(transaction)
        
    def change_transaction_status(self, transaction_id: str, new_status: PartyType):
        if new_status == "CREATED":
            raise HTTPException(400, "Status cannot be changed back to CREATED")
        
        transaction = self.get_transaction_service(transaction_id)
        if transaction.status == new_status:
            raise HTTPException(400, f"Transaction is already in status {new_status}")

        if new_status == "APPROVED":
            self.verify_approval_conditions(transaction)
            
        transaction.status = new_status
        return self.repository.update_status(transaction, new_status)
    
    def verify_approval_conditions(self, transaction: TransactionBase) -> bool:
        """
           Verifica se a transação tem os 3 registros obrigatórios:
           - 1 Vendedor (SELLER)
           - 1 Comprador (BUYER) 
           - 1 Corretor (BROKER)
       """
        party_types = {party.type for party in transaction.parties}
        required_types = {PartyType.SELLER, PartyType.BUYER, PartyType.BROKER}

        if not required_types.issubset(party_types):
            raise HTTPException(
                400, "Transaction must have at least one SELLER, one BUYER, and one BROKER to be approved"
            )
