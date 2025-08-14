# app/schema/auth.py
from pydantic import BaseModel, Field, validator
import re

class RegisterUser(BaseModel):
    """Schema for user registration"""
    email: str = Field(..., description="User's email address")
    username: str = Field(..., min_length=3, max_length=30, description="Username (3-30 characters)")
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")
    
    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username can only contain letters, numbers, underscores, and hyphens')
        return v.strip()
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        return v

class LoginUser(BaseModel):
    """Schema for user login"""
    email: str = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")
