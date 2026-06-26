"""
===============================================================================
AUTH CONFIG — fastapi-auth-module
===============================================================================
Central settings for the auth module.
Values are injected by mount_auth() at startup.
===============================================================================
"""

from pydantic_settings import BaseSettings


class AuthSettings(BaseSettings):
    DATABASE_URL: str = ""
    JWT_SECRET: str = ""
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    BCRYPT_ROUNDS: int = 12

    class Config:
        env_prefix = "AUTH_"


settings = AuthSettings()
