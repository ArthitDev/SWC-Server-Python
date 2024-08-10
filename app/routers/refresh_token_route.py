from fastapi import APIRouter, Depends, HTTPException, Response, Request, status
from sqlalchemy.orm import Session
from app.services.refresh_token_service import refresh_access_token
from app.db.database import get_db

router = APIRouter()


@router.post("/refresh-token")
def refresh_token(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refreshToken")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not provided",
        )
    return refresh_access_token(refresh_token, response)
