# fastapi-auth-module

Reusable authentication module for FastAPI projects.  
JWT tokens · bcrypt passwords · role-based access control · any SQL database.

---

## Features

- `POST /auth/register` — create an account
- `POST /auth/login` — get a JWT token
- `GET /auth/me` — get the current user
- `Depends(require_role("ADMIN"))` — protect any route by role
- Works with Supabase, PostgreSQL, SQLite, or any SQLAlchemy-compatible DB
- Extensible: add custom fields (sede_id, stripe_id, role…) via model inheritance

---

## Quick start

```bash
pip install -r requirements.txt
```

```python
# main.py
from fastapi import FastAPI
from auth import mount_auth

app = FastAPI()

mount_auth(
    app,
    db_url="postgresql://user:password@host/dbname",
    secret="your-jwt-secret-key",
)
```

That's it. Three endpoints are now live:

```
POST /api/v1/auth/register   → { "email": "...", "password": "..." }
POST /api/v1/auth/login      → { "access_token": "...", "token_type": "bearer" }
GET  /api/v1/auth/me         → { "id": "...", "email": "...", ... }
```

---

## Extend for your project

Add custom fields by inheriting from `BaseUser`:

```python
# your_project/models.py
from sqlalchemy import Column, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from auth.models import BaseUser
import enum

class RoleEnum(str, enum.Enum):
    CLIENT   = "CLIENT"
    EMPLOYEE = "EMPLOYEE"
    ADMIN    = "ADMIN"

class User(BaseUser):
    __tablename__ = "user"
    sede_id = Column(UUID(as_uuid=True), ForeignKey("sede.id"), nullable=True)
    role    = Column(Enum(RoleEnum), default=RoleEnum.CLIENT, nullable=False)
```

Then pass your model to `mount_auth`:

```python
from your_project.models import User

mount_auth(app, db_url="...", secret="...", user_model=User)
```

---

## Protect routes by role

```python
from fastapi import Depends
from auth import require_role, get_current_user

@router.get("/admin/dashboard")
def dashboard(user = Depends(require_role("ADMIN"))):
    return {"message": f"Welcome {user.email}"}

@router.get("/profile")
def profile(user = Depends(get_current_user)):
    return user
```

---

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `AUTH_JWT_SECRET` | — | JWT signing key |
| `AUTH_DATABASE_URL` | — | SQLAlchemy DB URL |
| `AUTH_ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | Token TTL (24h) |
| `AUTH_BCRYPT_ROUNDS` | `12` | bcrypt work factor |

---

## Project structure

```
auth/
├── __init__.py      # mount_auth() entry point
├── config.py        # settings
├── db.py            # session management
├── models.py        # BaseUser SQLAlchemy model
├── schemas.py       # Pydantic schemas
├── security.py      # bcrypt + JWT
├── service.py       # business logic
├── deps.py          # FastAPI dependencies
└── router.py        # API endpoints
```

---

## Tested with

- FastAPI 0.111+
- SQLAlchemy 2.0+
- Pydantic v2
- Supabase (PostgreSQL)
- Python 3.11+

---

## Used in

- [Idelette Beauty & Charme](https://github.com/MSimo1) — multi-sede beauty booking platform
