from httpx import AsyncClient, HTTPStatusError, Timeout
from pydantic import ValidationError

from app.core.config import settings
from app.services.chat_model import ChatCompletionResponse, ChatMessage


class OpenRouterClient:
    def __init__(self):
        self.base_url: str = settings.openrouter_base_url
        self.client: AsyncClient = AsyncClient(
            base_url=self.base_url, timeout=Timeout(30)
        )

    async def chat_completions(self, message: ChatMessage) -> ChatCompletionResponse:
        headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "HTTP-Referer": settings.openrouter_site_url,
            "X-OpenRouter-Title": settings.openrouter_app_name,
        }
        payload = {
            "model": settings.openrouter_model,
            "messages": [message.model_dump()],
        }
        print(payload)
        response = await self.client.post(
            "/chat/completions", json=payload, headers=headers
        )
        try:
            _ = response.raise_for_status()
            return ChatCompletionResponse.model_validate(response.json())
        except HTTPStatusError as e:
            print(e.response)
            raise Exception(f"Openrouter fucked off with code {e.response.status_code}")
        except ValidationError:
            raise Exception(f"Openrouter returned wierd response: {response.json()}")
