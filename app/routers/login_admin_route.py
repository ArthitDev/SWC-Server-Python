from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.schemas.login_admin import AdminLogin, AdminLoginResponse
from app.db.database import get_db
from app.services.login_admin_service import authenticate_admin

router = APIRouter()


@router.post("/login", response_model=AdminLoginResponse)
async def login_admin(
    admin_credentials: AdminLogin, response: Response, db: Session = Depends(get_db)
):
    return authenticate_admin(admin_credentials, db, response)
