from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Request
from app.models.admin import Admin
from app.schemas.register_admin import AdminCreate, AdminResponse
from passlib.context import CryptContext
import logging
import pendulum

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)


def get_password_hash(password: str) -> str:
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"Error hashing password: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


def create_admin(admin: AdminCreate, db: Session) -> AdminResponse:
    db_admin = (
        db.query(Admin)
        .filter((Admin.username == admin.username) | (Admin.email == admin.email))
        .first()
    )
    if db_admin:
        logger.error(
            f"Username or email already registered: {admin.username}, {admin.email}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered",
        )

    new_admin = Admin(
        username=admin.username,
        email=admin.email,
        password=get_password_hash(admin.password),
        created_at=pendulum.now("Asia/Bangkok"),
        updated_at=pendulum.now("Asia/Bangkok"),
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin


def register_admin(request: Request, admin: AdminCreate, db: Session) -> AdminResponse:
    try:
        return create_admin(admin, db)
    except HTTPException as e:
        if e.status_code == status.HTTP_400_BAD_REQUEST:
            logger.error(f"HTTPException: {e.detail}")
            raise e
        else:
            logger.error(f"Unexpected HTTPException: {e.detail}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
            )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
