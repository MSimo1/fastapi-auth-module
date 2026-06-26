"""
===============================================================================
AUTH SERVICE — fastapi-auth-module
===============================================================================
Business logic: register, authenticate, fetch user.
No HTTP logic here — that belongs in the router.
===============================================================================
"""

from sqlalchemy.orm import Session

from .models import BaseUser
from .schemas import RegisterRequest
from .security import hash_password, verify_password


def register_user(db: Session, data: RegisterRequest, user_model=None) -> BaseUser:
    """
    Create a new user.

    Args:
        db:         SQLAlchemy session
        data:       RegisterRequest schema
        user_model: Optional custom User model (defaults to BaseUser)
    """
    Model = user_model or BaseUser

    existing = db.query(Model).filter(Model.email == data.email).first()
    if existing:
        raise ValueError("Email already registered")

    user = Model(
        email=data.email,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str, user_model=None) -> BaseUser | None:
    """
    Verify credentials and return the user, or None if invalid.
    """
    Model = user_model or BaseUser
    user = db.query(Model).filter(Model.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def get_user_by_id(db: Session, user_id, user_model=None) -> BaseUser | None:
    """Fetch a user by their UUID."""
    Model = user_model or BaseUser
    return db.query(Model).filter(Model.id == user_id).first()
