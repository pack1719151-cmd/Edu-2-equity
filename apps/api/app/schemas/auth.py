from pydantic import BaseModel, EmailStr
from typing import Optional, Literal


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: Literal["student", "teacher", "principal"]  # enforced enum


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    is_active: bool
    role: str

    class Config:
        from_attributes = True


class UserMeResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    is_active: bool
    role: str

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    message: str

