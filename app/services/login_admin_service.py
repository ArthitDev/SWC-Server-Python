import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from dotenv import load_dotenv
from app.models.admin import Admin
from app.schemas.login_admin import AdminLogin

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret")
REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET", "your_refresh_token_secret")


def authenticate_admin(admin_credentials: AdminLogin, db: Session, response: Response):
    admin = db.query(Admin).filter(Admin.username == admin_credentials.username).first()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"
        )

    if not bcrypt.checkpw(
        admin_credentials.password.encode("utf-8"), admin.password.encode("utf-8")
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"
        )

    iat = datetime.utcnow()
    access_token_exp = iat + timedelta(hours=1)
    refresh_token_exp = iat + timedelta(days=7)

    access_token = jwt.encode(
        {
            "id": admin.id,
            "username": admin.username,
            "iat": iat,
            "exp": access_token_exp,
        },
        JWT_SECRET,
        algorithm="HS256",
    )
    refresh_token = jwt.encode(
        {
            "id": admin.id,
            "username": admin.username,
            "iat": iat,
            "exp": refresh_token_exp,
        },
        REFRESH_TOKEN_SECRET,
        algorithm="HS256",
    )

    response.set_cookie(
        key="accessToken", value=access_token, httponly=True, max_age=3600  # 1 hour
    )
    response.set_cookie(
        key="refreshToken", value=refresh_token, httponly=True, max_age=604800  # 7 days
    )

    return {"message": "เข้าสู่ระบบสำเร็จ"}
