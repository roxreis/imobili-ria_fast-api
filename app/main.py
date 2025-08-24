import os

from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import Base, engine
from app.routers import transacoes, partes, comissoes

API_SECRET_KEY = os.getenv("API_SECRET_KEY", "changeme123")
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Imobiliária")

security = HTTPBearer()

def check_auth(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != API_SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

app.include_router(transacoes.router, dependencies=[Depends(check_auth)])
app.include_router(partes.router, dependencies=[Depends(check_auth)])
app.include_router(comissoes.router, dependencies=[Depends(check_auth)])
