from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repository.commission import CommissionRepository
from app.models import Commission
from app.schemas import CommissionCreate
from app.interfaces.concrete.transaction_concrete import TransactionConcrete


class CommissionService:
    def __init__(self, db: Session, transaction_concrete: TransactionConcrete):
        self.repository = CommissionRepository(db)
        self.transaction_concrete = transaction_concrete

    def create_commission_service(self, commission_data: CommissionCreate) -> Commission:
        commission = commission_data.dict()
        calculated_amount = self.get_calculate_commission(commission)

        commission = Commission(
            transaction_id_fk=commission['transaction_id'],
            percentage=commission['percentage'],
            calculated_amount=calculated_amount,    
            paid=False
        )
        
        return self.repository.create_commission(commission)

    def pay_commission(self, commission_id: str) -> Commission:
        commission = self.repository.get_by_id(commission_id)
        if not commission:
            raise HTTPException(404, "Commission not found")
        commission.paid = True
        return self.repository.update(commission)

    def get_calculate_commission(self, commission: dict) -> float:
        transaction = self.transaction_concrete.get_transaction_service(commission['transaction_id'])
        if transaction.sale_value <= 0:
            raise HTTPException(400, "Sale value must be greater than zero to calculate commission")

        if not (0 < int(commission['percentage']) <= 100):
            raise HTTPException(400, "Percentage must be between 0 and 100")
        
        return transaction.sale_value * (commission['percentage'] / 100)
