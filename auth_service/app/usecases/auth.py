"""
В этом файле описывается бизнес-логика Auth Service. Здесь вы реализуете register(), login(), me(). Здесь вы проверяете, существует ли пользователь, хешируете пароль, проверяете пароль при логине, создаёте JWT, проверяете что пользователь существует для /me. При ошибках вы должны бросать ваши исключения из app/core/exceptions.py (например, UserAlreadyExistsError, InvalidCredentialsError, UserNotFoundError). Здесь не должно быть SQL-запросов напрямую — только вызовы репозитория.
"""

from datetime import datetime, timezone

from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError, InvalidCredentialsError
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import User
from app.repositories.users import UserRepository
from app.schemas.auth import RegisterRequest, TokenResponse


class AuthService:
    def __init__(self, user_repo: UserRepository):
        """Store the repository used for authentication operations."""
        self.user_repo = user_repo

    async def register(self, request: RegisterRequest) -> User:
        """Create a new user after verifying the email is not already taken."""
        existing_user = await self.user_repo.get_by_email(request.email)
        if existing_user:
            raise UserAlreadyExistsError()

        user = User(
            email=request.email,
            password_hash=hash_password(request.password),
            role="user",
            created_at=datetime.now(timezone.utc),
        )
        await self.user_repo.create(user)
        return user

    async def login(self, email: str, password: str) -> TokenResponse:
        """Validate user credentials and issue an access token."""
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()

        token = create_access_token(sub=str(user.id), role=user.role)
        return TokenResponse(access_token=token)

    async def me(self, user_id: int) -> User:
        """Return a user profile by id or raise if it does not exist."""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return user
