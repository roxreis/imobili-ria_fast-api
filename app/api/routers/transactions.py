import os

from fastapi import APIRouter, Depends, HTTPException, Header, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.database import get_db
from app.models import TransactionStatus
from app.service.transaction import TransactionService
from app.schemas import (
    TransactionCreate, TransactionOut, StatusUpdate,
    PartyCreate, PartyOut, CommissionCreate, CommissionOut, TransactionBase
)


load_dotenv()

router = APIRouter(tags=["transactions"])
security = HTTPBearer()
API_SECRET = os.getenv("API_SECRET_KEY")  

def get_transaction_service(db: Session = Depends(get_db)):
    return TransactionService(db)

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_SECRET:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")
    return True


@router.post("/api/v1/transactions", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
def create_transaction(
    payload: TransactionCreate,
    service: TransactionService = Depends(get_transaction_service),
    authenticated: bool = Depends(validate_token)
):
    return service.create_transaction_service(payload)

@router.get("/api/v1/transactions", response_model=List[TransactionOut])
def list_transactions(
    t_status: Optional[TransactionStatus] = None,
    property_code: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    response: Response = None,
    authenticated: bool = Depends(validate_token),
    service: TransactionService = Depends(get_transaction_service),
):
    filters = {}
    if t_status:
        filters["status"] = t_status
    if property_code:
        filters["property_code"] = property_code
    transactions = service.list_transactions_service(filters, limit, offset)
    total = len(transactions)
    if response:
        response.headers["X-Total-Count"] = str(total)
    return transactions

@router.get("/api/v1/transactions/{transaction_id}", response_model=TransactionOut)
def get_transaction(
    transaction_id: str,
    service: TransactionService = Depends(get_transaction_service),
    authenticated: bool = Depends(validate_token)
):
    return service.get_transaction_service(transaction_id)

@router.put("/api/v1/transactions/{transaction_id}", response_model=TransactionOut)
def update_transaction(
    transaction_id: str,
    payload: TransactionBase,
    service: TransactionService = Depends(get_transaction_service),
    authenticated: bool = Depends(validate_token)
):
    return service.update_transaction(transaction_id, payload)

@router.patch("/api/v1/transactions/{tx_id}/status", response_model=TransactionOut)
def update_status(
    tx_id: str,
    payload: StatusUpdate,
    service: TransactionService = Depends(get_transaction_service),
    authenticated: bool = Depends(validate_token)
):
    return service.change_status(tx_id, payload.new_status)

@router.delete("/api/v1/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    transaction_id: str,
    service: TransactionService = Depends(get_transaction_service),
    authenticated: bool = Depends(validate_token)
):
    service.delete_transaction(transaction_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
