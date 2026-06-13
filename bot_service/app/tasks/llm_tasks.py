import asyncio

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession

from app.core.config import settings
from app.infra.celery_app import celery_app
from app.services.chat_model import ChatCompletionResponse, ChatMessage
from app.services.openrouter_client import OpenRouterClient


@celery_app.task
def llm_request(tg_chat_id: int | str, prompt: str) -> None:
    async def _async_worker():
        client = OpenRouterClient()
        message = ChatMessage(role="user", content=prompt)

        response: ChatCompletionResponse = await client.chat_completions(message)

        answer_text = response.choices[0].message.content
        session = AiohttpSession(proxy=settings.http_proxy)

        bot = Bot(token=settings.telegram_bot_token, session=session)

        try:
            _ = await bot.send_message(chat_id=tg_chat_id, text=answer_text)
        finally:
            await bot.session.close()

    asyncio.run(_async_worker())
