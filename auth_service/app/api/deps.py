from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

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
    user_id = payload.sub
    return int(user_id)
