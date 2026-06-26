"""
===============================================================================
AUTH ROUTER — fastapi-auth-module
===============================================================================
Endpoints:
    POST /auth/register  — create account
    POST /auth/login     — get JWT token
    GET  /auth/me        — get current user
===============================================================================
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .db import get_db
from .deps import get_current_user
from .schemas import LoginRequest, RegisterRequest, TokenResponse, UserOut
from .security import create_access_token
from .service import authenticate_user, register_user


def create_auth_router(user_model=None, user_out_schema=None) -> APIRouter:
    """
    Factory that returns the auth router.
    Pass custom user_model or user_out_schema to extend behavior.
    """
    router = APIRouter()
    OutSchema = user_out_schema or UserOut

    @router.post("/register", response_model=OutSchema, status_code=status.HTTP_201_CREATED)
    def register(data: RegisterRequest, db: Session = Depends(get_db)):
        try:
            user = register_user(db, data, user_model=user_model)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        return user

    @router.post("/login", response_model=TokenResponse)
    def login(data: LoginRequest, db: Session = Depends(get_db)):
        user = authenticate_user(db, data.email, data.password, user_model=user_model)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        token = create_access_token({"sub": str(user.id)})
        return TokenResponse(access_token=token)

    @router.get("/me", response_model=OutSchema)
    def me(current_user=Depends(get_current_user)):
        return current_user

    return router
