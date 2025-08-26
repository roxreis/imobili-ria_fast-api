from sqlalchemy.orm import Session
from app.repository.commission import CommissionRepository
from app.models import Commission
from app.schemas import CommissionCreate
from fastapi import HTTPException

class CommissionService:
    def __init__(self, db: Session):
        self.repository = CommissionRepository(db)

    def create_commission(self, commission: CommissionCreate) -> Commission:
        commission = Commission(commission)
        if commission.amount <= 0:
            raise HTTPException(400, "Commission amount must be greater than zero")
        
        return self.repository.create(commission)

    def pay_commission(self, commission_id: str) -> Commission:
        commission = self.repository.get_by_id(commission_id)
        if not commission:
            raise HTTPException(404, "Commission not found")
        commission.paid = True
        return self.repository.update(commission)
