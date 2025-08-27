import os
import logging

from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers.transactions import router as transactions_router
from app.api.routers.parties import router as parties_router
from app.api.routers.comissions import router as commissions_router

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Imob Api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
API_SECRET_KEY = os.getenv("API_SECRET_KEY", "1234567890abcdef")


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.info("✅ Token válido")
    return credentials


@app.middleware("http")
async def auth_middleware(request, call_next):
    if request.url.path not in ["/", "/health", "/docs", "/redoc", "/openapi.json"]:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid or missing token")

        token = auth_header.replace("Bearer ", "")
        if token.strip() != API_SECRET_KEY.strip():
            raise HTTPException(status_code=401, detail="Invalid or missing token")

    response = await call_next(request)
    return response

app.include_router(transactions_router, prefix="/api/v1/transactions", tags=["transactions"])
app.include_router(parties_router, prefix="/api/v1", tags=["parties"])
app.include_router(commissions_router, prefix="/api/v1", tags=["commissions"])

@app.get("/")
async def root():
    return {"message": "PipeImob API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
