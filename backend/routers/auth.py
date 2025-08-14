# app/routes/auth.py
from fastapi import APIRouter, HTTPException
from db.database import supabase
from schemas.auth import RegisterUser, LoginUser
from models.user import UserResponse, AuthTokens

router = APIRouter(tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
def register(user: RegisterUser):
    try:
        # Create user in Supabase with metadata
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {"username": user.username}
            }
        })

        if not response.user:
            raise HTTPException(status_code=400, detail="Registration failed")

        

        # Extract username from metadata
        username = response.user.user_metadata.get("username", "")

        return UserResponse(
            id=response.user.id,
            email=response.user.email,
            username=username
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login", response_model=AuthTokens)
def login(user: LoginUser):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })

        if not response.user:
            raise HTTPException(status_code=400, detail="Invalid credentials")


        return AuthTokens(
            access_token=response.session.access_token,
            refresh_token=response.session.refresh_token
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
