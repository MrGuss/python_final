import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_register_login_and_me_flow(client: AsyncClient):
    register_response = await client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "strong-password"},
    )
    assert register_response.status_code == 200
    registered_user = register_response.json()  # pyright: ignore[reportAny]
    assert registered_user["email"] == "user@example.com"
    assert registered_user["role"] == "user"

    login_response = await client.post(
        "/auth/login",
        data={"username": "user@example.com", "password": "strong-password"},
    )
    assert login_response.status_code == 200
    token_payload = login_response.json()  # pyright: ignore[reportAny]
    assert token_payload["token_type"] == "bearer"
    assert token_payload["access_token"]

    me_response = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token_payload['access_token']}"},
    )
    assert me_response.status_code == 200
    assert me_response.json() == registered_user


async def test_register_existing_email_returns_409(client: AsyncClient):
    payload = {"email": "duplicate@example.com", "password": "strong-password"}

    first_response = await client.post("/auth/register", json=payload)
    second_response = await client.post("/auth/register", json=payload)

    assert first_response.status_code == 200
    assert second_response.status_code == 409


async def test_login_with_wrong_password_returns_401(client: AsyncClient):
    await client.post(
        "/auth/register",
        json={"email": "login@example.com", "password": "strong-password"},
    )

    response = await client.post(
        "/auth/login",
        data={"username": "login@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401


async def test_me_without_token_returns_401(client: AsyncClient):
    response = await client.get("/auth/me")

    assert response.status_code == 401


async def test_me_with_invalid_token_returns_401(client: AsyncClient):
    response = await client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401
