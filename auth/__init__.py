"""
===============================================================================
fastapi-auth-module
===============================================================================
Reusable authentication module for FastAPI projects.
Provides JWT auth, bcrypt password hashing, and role-based access control.

Usage:
    from auth import mount_auth
    mount_auth(app, db_url="postgresql://...", secret="your-secret")
===============================================================================
"""

from .router import create_auth_router
from .models import BaseUser
from .deps import get_current_user, require_role
from .security import hash_password, verify_password, create_access_token


def mount_auth(app, db_url: str, secret: str, prefix: str = "/api/v1/auth"):
    """
    Mount the auth module onto a FastAPI app.

    Args:
        app:      FastAPI application instance
        db_url:   Database URL (postgresql, sqlite, etc.)
        secret:   JWT secret key
        prefix:   URL prefix for auth endpoints (default: /api/v1/auth)
    """
    from .config import settings as auth_settings
    from .db import init_db

    auth_settings.DATABASE_URL = db_url
    auth_settings.JWT_SECRET = secret

    init_db(db_url)

    router = create_auth_router()
    app.include_router(router, prefix=prefix, tags=["auth"])


__all__ = [
    "mount_auth",
    "BaseUser",
    "get_current_user",
    "require_role",
    "hash_password",
    "verify_password",
    "create_access_token",
]
