import time

import bcrypt
import jwt
from pydantic import ValidationError

from app.core.config import settings
from app.core.exceptions import InvalidTokenError, TokenExpiredError
from app.core.jwt_model import JwtPayload


def hash_password(password: str) -> str:
    """Hash a plain-text password with bcrypt."""
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check whether a plain-text password matches a stored hash."""
    password_byte_enc = plain_password.encode("utf-8")
    return bcrypt.checkpw(
        password=password_byte_enc, hashed_password=hashed_password.encode("utf-8")
    )


def _now() -> int:
    """Return the current UNIX timestamp in seconds."""
    return int(time.time())


def create_access_token(sub: str, role: str) -> str:
    """Build and sign an access token for the given subject."""
    payload = JwtPayload(
        sub=sub,
        type="access",
        role=role,
        iat=_now(),
        exp=_now() + settings.access_token_expire_minutes * 60,
    )
    return jwt.encode(
        payload.model_dump(), settings.jwt_secret, algorithm=settings.jwt_alg
    )


def decode_token(token: str) -> JwtPayload:
    """Decode and validate a JWT token."""
    try:
        return JwtPayload.model_validate(
            jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
        )
    except ValidationError:
        raise InvalidTokenError("Invalid parameters in decoded token")
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError()
    except Exception as e:
        raise InvalidTokenError(f"{e}")
