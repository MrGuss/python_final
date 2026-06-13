from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        """Store the async database session used by the repository."""
        self._session: AsyncSession = session

    async def get_by_email(self, email: str) -> User | None:
        """Fetch a user by email address."""
        result = await self._session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_by_id(self, user_id: int) -> User | None:
        """Fetch a user by primary key."""
        result = await self._session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def create(self, user: User) -> User:
        """Persist a new user and return the refreshed model."""
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user
