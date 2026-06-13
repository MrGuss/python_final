import jwt
from pydantic import ValidationError

from app.core.config import settings
from app.core.jwt_model import JwtPayload


def decode_and_validate(token: str) -> JwtPayload:
    """Decode and validate a JWT token."""
    try:
        return JwtPayload.model_validate(
            jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_alg])
        )
    except ValidationError:
        raise ValueError("Invalid parameters in decoded token")
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except Exception as e:
        raise ValueError(f"Weird error: {e}")
