"""
В этом файле реализуются функции безопасности. Здесь вы настраиваете bcrypt через passlib, реализуете hash_password() и verify_password(). Здесь же реализуете create_access_token() и decode_token(). В create_access_token() вы обязаны формировать токен с полями sub, role, iat, exp. В decode_token() вы должны корректно валидировать подпись и время жизни токена. В usecase-логике и в deps вы будете использовать эти функции как готовые строительные блоки.
"""

import time
from typing import Any, Dict

import bcrypt
import jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    """Hash a plain-text password with bcrypt."""
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check whether a plain-text password matches a stored hash."""
    password_byte_enc = plain_password.encode("utf-8")
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password.encode("utf-8"))


def _now() -> int:
    """Return the current UNIX timestamp in seconds."""
    return int(time.time())


def create_access_token(sub: str, role: str) -> str:
    """Build and sign an access token for the given subject."""
    payload = {
        "sub": sub,
        "type": "access",
        "role": role,
        "iat": _now(),
        "exp": _now() + settings.access_token_expire_minutes * 60,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)


def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT token."""
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
