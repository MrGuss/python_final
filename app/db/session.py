"""
В этом файле создаётся асинхронный engine SQLAlchemy и фабрика сессий async_sessionmaker. Здесь вы должны собрать строку подключения из настроек, создать create_async_engine(...), создать AsyncSessionLocal. Этот файл не должен открывать сессию “сразу”. Он должен предоставлять инструменты для открытия сессии через dependencies.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

engine = create_async_engine(f"sqlite+aiosqlite:///{settings.sqlite_path}")
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession)
