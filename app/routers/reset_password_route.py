from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.reset_password_service import PasswordResetService
from app.schemas.reset_password import PasswordResetRequest, PasswordResetConfirm

router = APIRouter()


@router.post("/request-reset-password")
async def request_reset_password(
    request: PasswordResetRequest, db: Session = Depends(get_db)
):
    service = PasswordResetService(db)
    await service.request_reset_password(request.email)
    return {"msg": "Password reset link sent"}


@router.post("/reset-password")
async def reset_password(request: PasswordResetConfirm, db: Session = Depends(get_db)):
    service = PasswordResetService(db)
    await service.reset_password(request.token, request.newPassword)
    return {"msg": "Password has been reset"}
