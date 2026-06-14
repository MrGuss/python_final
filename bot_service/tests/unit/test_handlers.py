from __future__ import annotations

import fakeredis.aioredis
import pytest

from app.bot import handlers
from tests.conftest import DummyMessage


@pytest.fixture
async def fake_redis():
    redis = fakeredis.aioredis.FakeRedis()
    try:
        yield redis
    finally:
        await redis.aclose()


@pytest.mark.asyncio
async def test_token_command_stores_valid_token(
    fake_redis: fakeredis.aioredis.FakeRedis,
    mocker,
    valid_jwt: str,
) -> None:
    mocker.patch.object(handlers, "get_redis", return_value=fake_redis)
    message = DummyMessage(f"/token {valid_jwt}", user_id=42)

    await handlers.cmd_set_token(message)

    stored_token = await fake_redis.get(handlers.get_token_key(42))
    assert stored_token == valid_jwt.encode("utf-8")
    assert "Токен успешно сохранен" in str(message.answers[-1]["text"])


@pytest.mark.asyncio
async def test_text_without_token_does_not_call_celery(
    fake_redis: fakeredis.aioredis.FakeRedis,
    mocker,
) -> None:
    mocker.patch.object(handlers, "get_redis", return_value=fake_redis)
    delay = mocker.patch.object(handlers.llm_request, "delay")
    message = DummyMessage("hello", user_id=42, chat_id=900)

    await handlers.handle_text_message(message)

    delay.assert_not_called()
    assert "Токен не найден" in str(message.answers[-1]["text"])


@pytest.mark.asyncio
async def test_text_with_token_calls_celery(
    fake_redis: fakeredis.aioredis.FakeRedis,
    mocker,
    valid_jwt: str,
) -> None:
    mocker.patch.object(handlers, "get_redis", return_value=fake_redis)
    delay = mocker.patch.object(handlers.llm_request, "delay")
    await fake_redis.set(handlers.get_token_key(42), valid_jwt)
    message = DummyMessage("hello LLM", user_id=42, chat_id=900)

    await handlers.handle_text_message(message)

    delay.assert_called_once_with(tg_chat_id=900, prompt="hello LLM")
    assert "Ваш запрос принят" in str(message.answers[-1]["text"])
