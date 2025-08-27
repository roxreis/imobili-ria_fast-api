
import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from app.database import get_db
from app.service.commision import CommissionService
from app.service.transaction import get_concrete_transaction_service
from app.schemas import CommissionCreate, CommissionOut
from app.interfaces.concrete.transaction_concrete import TransactionConcrete


load_dotenv()

router = APIRouter(tags=["commissions"])
API_SECRET = os.getenv("API_SECRET_KEY")  
security = HTTPBearer()

def get_service(service_class: str):
    return globals()[service_class]()

def get_commission_service(
    db = Depends(get_db),
    transaction_concrete: TransactionConcrete = Depends(get_concrete_transaction_service)
):
    return CommissionService(db, transaction_concrete)

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_SECRET:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")
    return True

@router.post("/", response_model=CommissionOut, status_code=status.HTTP_201_CREATED)
def create_commission(
    payload: CommissionCreate, 
    service: CommissionService = Depends(get_commission_service),
    authenticated: bool = Depends(validate_token)
):
    return service.create_commission_service(payload)

@router.post("/{commission_id}/pay", response_model=CommissionOut)
def pay_commission(
        commission_id: str, 
        service: CommissionService = Depends(get_commission_service),
        authenticated: bool = Depends(validate_token)
):
    return service.pay_commission(commission_id)
