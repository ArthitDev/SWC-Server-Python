from fastapi import Depends, HTTPException, status, Request
from jose import JWTError, jwt
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"


class JwtPayload(BaseModel):
    id: int
    username: str


def authenticate_token(request: Request) -> JwtPayload:
    token = request.cookies.get("accessToken")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        username: str = payload.get("username")
        if user_id is None or username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        return JwtPayload(id=user_id, username=username)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


async def get_current_user(token: JwtPayload = Depends(authenticate_token)):
    return token
