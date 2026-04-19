"""
В этом файле создаётся приложение FastAPI. Здесь вы собираете приложение как “композицию”: подключаете роутеры, подключаете обработчики исключений, подключаете lifespan (если вы хотите убрать deprecated warning от on_event) и добавляете базовые системные ручки, например /health. Здесь не пишется бизнес-логика и не пишется SQL. Здесь только конфигурация приложения и подключение модулей.
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes_auth import router as auth_router
from app.db.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and dispose application resources around the app lifecycle."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="Chat Application", lifespan=lifespan)


app.include_router(auth_router)


@app.get("/health")
async def health_check():
    """Return a basic service health payload."""
    return {"status": "healthy", "environment": os.getenv("ENVIRONMENT", "development"), "database": "sqlite"}
