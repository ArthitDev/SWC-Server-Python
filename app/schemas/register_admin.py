# app/schemas/admin.py

from pydantic import BaseModel, EmailStr
from datetime import datetime


class AdminCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class AdminResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
