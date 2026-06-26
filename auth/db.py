"""
===============================================================================
AUTH DB — fastapi-auth-module
===============================================================================
Database session management.
Compatible with any SQLAlchemy-supported database.
===============================================================================
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

_engine = None
_SessionLocal = None


def init_db(db_url: str):
    """Initialize the database engine and create tables."""
    global _engine, _SessionLocal

    connect_args = {}
    if db_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}

    _engine = create_engine(db_url, connect_args=connect_args)
    _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

    # Create tables
    from .models import Base
    Base.metadata.create_all(bind=_engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency — yields a DB session."""
    if _SessionLocal is None:
        raise RuntimeError("Database not initialized. Call mount_auth() first.")
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()
