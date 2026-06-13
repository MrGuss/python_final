from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

from app.bot.handlers import router
from app.core.config import settings

session = AiohttpSession(proxy=settings.http_proxy)

bot = Bot(token=settings.telegram_bot_token, session=session)

dp = Dispatcher()
dp.include_router(router)
