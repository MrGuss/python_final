from __future__ import annotations

import json

import pytest
import respx
from httpx import Response

from app.core.config import settings
from app.services.chat_model import ChatMessage
from app.services.openrouter_client import OpenRouterClient


@pytest.mark.asyncio
@respx.mock
async def test_chat_completions_posts_payload_and_extracts_response() -> None:
    route = respx.post(f"{settings.openrouter_base_url}/chat/completions").mock(
        return_value=Response(
            200,
            json={
                "id": "chatcmpl-test",
                "object": "chat.completion",
                "created": 1,
                "model": settings.openrouter_model,
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": "test response"},
                        "finish_reason": "stop",
                    }
                ],
                "usage": {
                    "prompt_tokens": 2,
                    "completion_tokens": 3,
                    "total_tokens": 5,
                },
                "system_fingerprint": None,
            },
        )
    )
    client = OpenRouterClient()

    try:
        response = await client.chat_completions(
            ChatMessage(role="user", content="hello")
        )
    finally:
        await client.client.aclose()

    assert route.called
    request = route.calls.last.request
    assert request.headers["Authorization"] == f"Bearer {settings.openrouter_api_key}"
    assert request.headers["HTTP-Referer"] == settings.openrouter_site_url
    assert request.headers["X-OpenRouter-Title"] == settings.openrouter_app_name
    assert json.loads(request.content) == {
        "model": settings.openrouter_model,
        "messages": [{"role": "user", "content": "hello"}],
    }
    assert response.choices[0].message.content == "test response"
