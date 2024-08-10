from pydantic import BaseModel


class AdminLogin(BaseModel):
    username: str
    password: str


class AdminLoginResponse(BaseModel):
    message: str
