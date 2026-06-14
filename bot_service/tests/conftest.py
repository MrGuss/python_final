from __future__ import annotations

import time
from dataclasses import dataclass

import jwt
import pytest

from app.core.config import settings


@dataclass
class DummyUser:
    id: int


@dataclass
class DummyChat:
    id: int


class DummyMessage:
    def __init__(self, text: str | None, user_id: int = 123, chat_id: int = 456):
        self.text = text
        self.from_user = DummyUser(id=user_id)
        self.chat = DummyChat(id=chat_id)
        self.answers: list[dict[str, object]] = []

    async def answer(self, text: str, **kwargs: object) -> None:
        self.answers.append({"text": text, **kwargs})


@pytest.fixture
def jwt_payload() -> dict[str, int | str]:
    now = int(time.time())
    return {
        "sub": "user-1",
        "type": "access",
        "role": "user",
        "iat": now,
        "exp": now + 3600,
    }


@pytest.fixture
def valid_jwt(jwt_payload: dict[str, int | str]) -> str:
    return jwt.encode(jwt_payload, settings.jwt_secret, algorithm=settings.jwt_alg)

