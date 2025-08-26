import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Header, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.service.party import PartyService
from app.schemas import PartyCreate, PartyOut


load_dotenv()

security = HTTPBearer()
API_SECRET = os.getenv("API_SECRET_KEY")  

def get_party_service(db: Session = Depends(get_db)):
    return PartyService(db)

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_SECRET:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")
    return True

router = APIRouter(tags=["parties"])

@router.post("/", response_model=PartyOut, status_code=status.HTTP_201_CREATED)
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
