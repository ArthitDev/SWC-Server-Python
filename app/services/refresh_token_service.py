import os
from jose import JWTError, jwt
from fastapi import HTTPException, status, Response
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app.schemas.login_admin import AdminLogin
from app.schemas.token_admin import Token, TokenData  # Update this line

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret")
REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET", "your_refresh_token_secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    iat = datetime.utcnow()
    to_encode.update({"exp": expire, "iat": iat})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    iat = datetime.utcnow()
    to_encode.update({"exp": expire, "iat": iat})
    encoded_jwt = jwt.encode(to_encode, REFRESH_TOKEN_SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def refresh_access_token(refresh_token: str, response: Response):
    try:
        payload = jwt.decode(
            refresh_token, REFRESH_TOKEN_SECRET, algorithms=[ALGORITHM]
        )
        username: str = payload.get("username")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )
        token_data = TokenData(username=username)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id": user_id, "username": token_data.username},
        expires_delta=access_token_expires,
    )
    response.set_cookie(
        key="accessToken", value=access_token, httponly=True, max_age=3600  # 1 hour
    )
    return {"access_token": access_token, "token_type": "bearer"}
