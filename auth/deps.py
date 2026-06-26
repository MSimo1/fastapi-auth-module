"""
===============================================================================
AUTH DEPS — fastapi-auth-module
===============================================================================
FastAPI dependencies for JWT verification and role-based access control.

Usage in any route:
    @router.get("/admin")
    def admin_only(user = Depends(require_role("ADMIN"))):
        ...
===============================================================================
"""

from typing import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from .db import get_db
from .security import decode_token
from .service import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """Dependency: returns the authenticated user or raises 401."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_id(db, user_id)
    if user is None or not user.is_active:
        raise credentials_exception
    return user


def require_role(*roles: str) -> Callable:
    """
    Dependency factory: requires the user to have one of the specified roles.

    Example:
        Depends(require_role("ADMIN", "EMPLOYEE"))
    """
    def _checker(current_user=Depends(get_current_user)):
        user_role = getattr(current_user, "role", None)
        if user_role is None or str(user_role) not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access restricted to: {', '.join(roles)}",
            )
        return current_user
    return _checker
