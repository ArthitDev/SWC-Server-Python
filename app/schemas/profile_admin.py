from pydantic import BaseModel, EmailStr


class JwtPayload(BaseModel):
    id: int
    username: str


class AdminProfileResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    message: str
