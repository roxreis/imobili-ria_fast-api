from sqlalchemy.orm import Session
from app.models import Commission


class CommissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_commission(self, commission: Commission):
        self.db.add(commission)
        self.db.commit()
        self.db.refresh(commission)
        return commission

    def get_by_id(self, commission_id: str):
        return self.db.query(Commission).filter_by(id=commission_id).first()

    def update(self, commission: Commission):
        self.db.commit()
        self.db.refresh(commission)
        return commission
