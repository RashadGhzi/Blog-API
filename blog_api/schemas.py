from pydantic import BaseModel, EmailStr
from datetime import datetime
from fastapi import UploadFile, File
from typing import Dict



class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    hashed_password: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str

class PostReponse(BaseModel):
    id: int
    title: str
    content: str
    user_email: str
    created_at: datetime
    updated_at: datetime
    user: UserResponse

    class Config:
        from_attributes = True