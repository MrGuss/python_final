from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

engine = create_async_engine(f"sqlite+aiosqlite:///{settings.sqlite_path}")
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession)
