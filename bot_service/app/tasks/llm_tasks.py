import asyncio

from aiogram import Bot
from celery import shared_task

from app.core.config import settings
from app.services.chat_model import ChatCompletionResponse, ChatMessage
from app.services.openrouter_client import OpenRouterClient


@shared_task
def llm_request(tg_chat_id: int | str, prompt: str) -> None:
    async def _async_worker():
        client = OpenRouterClient()
        message = ChatMessage(role="user", content=prompt)

        response: ChatCompletionResponse = await client.chat_completions(message)

        answer_text = response.choices[0].message.content

        bot = Bot(token=settings.telegram_bot_token)
        try:
            _ = await bot.send_message(chat_id=tg_chat_id, text=answer_text)
        finally:
            await bot.session.close()

    asyncio.run(_async_worker())
