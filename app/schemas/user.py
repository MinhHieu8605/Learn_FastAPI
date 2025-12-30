from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserBase(BaseModel):
    user_name: str
    email: EmailStr
    full_name: str
    phone_number: str
    status: int

    class Config:
        from_attributes = True

class UserSearchRequest(BaseModel):
    user_name: Optional[str] = None
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    status: Optional[int] = None
    roles: Optional[List[str]] = None

class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=64)
    roles: List[str]

class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    status: Optional[int] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    roles: Optional[List[str]] = None

class UserInDB(UserBase):
    id: int
    created_at: datetime 

    class Config:
        from_attributes = True

class UserResponse(UserInDB):
    roles: List[str] = []
    class Config:
        from_attributes = True




