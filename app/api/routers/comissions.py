
import os

from fastapi import APIRouter, Depends, HTTPException, Header, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.main import verify_token
from app.database import get_db
from app.service.commision import CommissionService
from app.schemas import CommissionCreate, CommissionOut


load_dotenv()

def get_commission_service(db: Session = Depends(get_db)):
    return CommissionService(db)

router = APIRouter(tags=["commissions"])
API_SECRET = os.getenv("API_SECRET_KEY")  

@router.post("/", response_model=CommissionOut, status_code=status.HTTP_201_CREATED)
def create_commission(
    commission: CommissionCreate, 
    service: CommissionService = Depends(get_commission_service),
    authenticated: bool = Depends(verify_token)
):
    return service.create_commission(commission)

@router.post("/{commission_id}/pay", response_model=CommissionOut)
def pay_commission(
        commission_id: str, 
        service: CommissionService = Depends(get_commission_service),
        authenticated: bool = Depends(verify_token)
):
    return service.pay_commission(commission_id)
