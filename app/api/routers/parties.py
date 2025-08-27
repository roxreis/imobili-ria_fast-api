import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Header, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.service.party import PartyService
from app.schemas import PartyCreate, PartyOut

from app.service.transaction import get_concrete_transaction_service
from app.interfaces.concrete.transaction_concrete import TransactionConcrete


load_dotenv()

security = HTTPBearer()
API_SECRET = os.getenv("API_SECRET_KEY")  

def get_service(service_class: str):
    return globals()[service_class]()

def get_party_service(
    db = Depends(get_db),
    transaction_concrete: TransactionConcrete = Depends(get_concrete_transaction_service)
):
    return PartyService(db, transaction_concrete)

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_SECRET:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")
    return True

router = APIRouter(tags=["parties"])

@router.post("/transactions/{transaction_id}/parties", response_model=PartyOut, status_code=status.HTTP_201_CREATED)
def add_party(
        party: PartyCreate, 
        service: PartyService = Depends(get_party_service),
        authenticated: bool = Depends(validate_token)
):
    return service.add_party_service(party)

@router.delete("/{party_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_party(
        party_id: str, 
        service: PartyService = Depends(get_party_service),
        authenticated: bool = Depends(validate_token)
):
    service.remove_party(party_id)
