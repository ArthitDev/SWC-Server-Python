from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.register_admin import AdminCreate, AdminResponse
from app.services.register_admin_service import register_admin
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
logger = logging.getLogger(__name__)

@router.post("/register", response_model=AdminResponse, status_code=201)
@limiter.limit("5/minute")
async def register(request: Request, admin: AdminCreate, db: Session = Depends(get_db)):
    return register_admin(request, admin, db)
