"""
В этом файле реализуются зависимости FastAPI. Здесь должна быть зависимость get_db() для выдачи AsyncSession. Здесь же должны быть фабрики get_users_repo() и get_auth_uc(). Здесь же реализуется зависимость get_current_user_id()/get_current_user() которая берёт токен из Authorization: Bearer ..., декодирует токен, проверяет валидность и возвращает user_id или пользователя. При ошибках токена вы бросаете InvalidTokenError/TokenExpiredError.
"""

from typing import Annotated
import time

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InvalidTokenError, TokenExpiredError
from app.core.security import decode_token
from app.db.session import AsyncSessionLocal
from app.repositories.users import UserRepository
from app.usecases.auth import AuthService


async def get_db():
    """Yield a database session for a request scope."""
    async with AsyncSessionLocal() as session:
        yield session


def get_user_repo(session: Annotated[AsyncSession, Depends(get_db)]):
    """Create a user repository bound to the current session."""
    return UserRepository(session)


def get_auth_uc(user_repo: Annotated[UserRepository, Depends(get_user_repo)]):
    """Create an authentication service for the current request."""
    return AuthService(user_repo)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)]) -> int:
    """Extract and validate the current user id from the bearer token."""
    payload = decode_token(token)
    user_id = payload.get("sub")
    expires = payload.get("exp")
    if user_id is None:
        raise InvalidTokenError()
    if expires is None or expires < time.time():
        raise TokenExpiredError()
    return int(user_id)
