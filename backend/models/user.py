# app/models/user.py
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: str
    email: str
    username: str  # Added username

    class Config:
        from_attributes = True

class AuthTokens(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
