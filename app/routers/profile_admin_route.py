from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.middlewares.authMiddleware import get_current_user
from app.schemas.profile_admin import AdminProfileResponse
from app.services.profile_admin_service import get_admin_profile

router = APIRouter()


@router.get("/profile", response_model=AdminProfileResponse)
async def read_admin_profile(
    current_user=Depends(get_current_user), db: Session = Depends(get_db)
):
    return get_admin_profile(current_user, db)
