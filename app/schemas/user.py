from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password is too short")
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password is too long")
        return v

class UserResponse(BaseModel):
    id: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password is too short")
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password is too long")
        return v

class Token(BaseModel):
    access_token: str
    token_type: str