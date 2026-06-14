from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_auth_uc, get_current_user_id
from app.core.exceptions import InternalServerError
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthService

router = APIRouter()


@router.post("/auth/register")
async def register(
    register_request: RegisterRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_uc)],
):
    """Register a new user account."""
    try:
        user = await auth_service.register(register_request)
        return UserPublic.model_validate(user)
    except HTTPException:
        raise
    except Exception as e:
        raise InternalServerError(detail=str(e))


@router.post("/auth/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(get_auth_uc)],
) -> TokenResponse:
    """Authenticate a user and return an access token."""
    try:
        token_response = await auth_service.login(
            form_data.username, form_data.password
        )
        return token_response
    except HTTPException:
        raise
    except Exception as e:
        raise InternalServerError(detail=str(e))


@router.get("/auth/me")
async def get_current_user(
    user_id: Annotated[int, Depends(get_current_user_id)],
    auth_service: Annotated[AuthService, Depends(get_auth_uc)],
):
    """Return the authenticated user's public profile."""
    try:
        user = await auth_service.me(user_id)
        return UserPublic.model_validate(user)
    except HTTPException:
        raise
    except Exception as e:
        raise InternalServerError(detail=str(e))
