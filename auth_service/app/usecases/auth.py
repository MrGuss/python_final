from datetime import datetime, timezone

from app.core.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import User
from app.repositories.users import UserRepository
from app.schemas.auth import RegisterRequest, TokenResponse


class AuthService:
    def __init__(self, user_repo: UserRepository):
        """Store the repository used for authentication operations."""
        self.user_repo: UserRepository = user_repo

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
        user_ret = await self.user_repo.create(user)
        return user_ret

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
