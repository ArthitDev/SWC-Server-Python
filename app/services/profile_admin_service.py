from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.admin import Admin
from app.schemas.profile_admin import AdminProfileResponse


def get_admin_profile(current_user, db: Session) -> AdminProfileResponse:
    admin = db.query(Admin).filter(Admin.id == current_user.id).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found",
        )
    return AdminProfileResponse(
        id=admin.id,
        username=admin.username,
        email=admin.email,
        message="Profile retrieved successfully",
    )
