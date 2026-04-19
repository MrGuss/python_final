"""
В этом файле описываются pydantic-схемы для регистрации и токенов. Здесь должна быть модель входа RegisterRequest с email и password, и модель ответа TokenResponse с access_token и token_type. Здесь же можно описать LoginResponse, если вы отдаёте токен отдельно. Важно: для /auth/login вы используете OAuth2PasswordRequestForm, поэтому pydantic-модель входа для логина может не требоваться.
"""

from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=8, max_length=50)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
