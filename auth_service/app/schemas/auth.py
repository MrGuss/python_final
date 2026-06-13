from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    email: str = Field(min_length=1)
    password: str = Field(min_length=8, max_length=50)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
