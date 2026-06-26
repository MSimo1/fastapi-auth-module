"""
===============================================================================
AUTH MODELS — fastapi-auth-module
===============================================================================
BaseUser: minimal SQLAlchemy model.
Extend it in your project to add custom fields (sede_id, stripe_id, etc.)

Example (Idelette):
    from auth.models import BaseUser
    class User(BaseUser):
        __tablename__ = "user"
        sede_id = Column(UUID, ForeignKey("sede.id"))
        role    = Column(Enum(RoleEnum), default="CLIENT")
===============================================================================
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class BaseUser(Base):
    """
    Minimal user model. Override __tablename__ and add columns in your project.
    """
    __tablename__ = "auth_user"
    __abstract__ = False  # Set True in your subclass to use a different table

    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email      = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active  = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
