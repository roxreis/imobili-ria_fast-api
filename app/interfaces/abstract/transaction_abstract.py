from uuid import UUID
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from app.schemas import TransactionCreate
from app.models import Transaction
    
class TransactionInterface(ABC):
    @abstractmethod
    def create_transaction_service(
            self, transaction_data: TransactionCreate
    ) -> Transaction:
        pass

    @abstractmethod
    def get_transaction_service(
            self, transaction_id: UUID | str
    ) -> Transaction:
        pass
    
    @abstractmethod
    def list_transactions_service(
            self,
            filters: dict,
            limit: int = 10, 
            offset: int = 0
    ):
        pass