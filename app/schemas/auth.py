from typing import List

from pydantic import BaseModel, field_validator


class LoginRequest(BaseModel):
    user_name: str
    password: str

class RegisterRequest(BaseModel):
    user_name: str
    full_name: str
    email: str
    phone_number: str
    password: str
    confirm_password: str
    status: int

    @field_validator('confirm_password')
    def password_match(cls, value, info):
        if "password" in info.data and value != info.data["password"]:
            raise ValueError('Passwords do not match')
        return value

class RegisterResponse(BaseModel):
    id: int
    user_name: str
    full_name: str
    phone_number: str
    email: str
    status: int

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token: str


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    user_name: str
    role: List[str]
    exp: int
    type: str


