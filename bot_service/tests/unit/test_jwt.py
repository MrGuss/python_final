from __future__ import annotations

import pytest

from app.core.jwt import decode_and_validate


def test_decode_and_validate_extracts_sub(valid_jwt: str) -> None:
    payload = decode_and_validate(valid_jwt)

    assert payload.sub == "user-1"


def test_decode_and_validate_rejects_garbage_token() -> None:
    with pytest.raises(ValueError):
        decode_and_validate("not-a-jwt")

