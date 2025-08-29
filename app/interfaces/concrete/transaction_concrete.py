from typing import TYPE_CHECKING
from app.schemas import TransactionCreate
from app.interfaces.abstract.transaction_abstract import TransactionInterface
from app.models import Transaction


class TransactionConcrete(TransactionInterface):
    def __init__(self, db):
        from app.service.transaction import TransactionService
        self.service = TransactionService(db)

    def create_transaction_service(self, transaction_data: TransactionCreate) -> Transaction:
        return self.service.create_transaction_service(transaction_data)

    def get_transaction_service(self, transaction_id):
        return self.service.get_transaction_service(transaction_id)
    
    def list_transactions_service(self, filters, limit=10, offset=0):
        return self.service.list_transactions_service(filters, limit, offset)
