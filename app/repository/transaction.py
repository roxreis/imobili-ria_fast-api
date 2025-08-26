from typing import Any

from sqlalchemy.orm import Session
from app.models import Transaction


class TransactionRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_transaction(self, transaction: Transaction) -> Transaction:
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def get_transaction_by_id(self, transaction_id: str) -> Transaction | None:
        return self.session.query(Transaction).filter_by(transaction_id=transaction_id).first()

    def list_transactions_repository(self, filters: dict, limit: int, offset: int) -> list[type[Transaction]]:
        query = self.session.query(Transaction)
        if 'status' in filters:
            query = query.filter(Transaction.status == filters['status'])
        if 'property_code' in filters:
            query = query.filter(Transaction.property_code == filters['property_code'])

        return query.offset(offset).limit(limit).all()

    def update(self, transaction: Transaction) -> Transaction:
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def delete(self, transaction: Transaction) -> None:
        self.session.delete(transaction)
        self.session.commit()      

