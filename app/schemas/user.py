"""
В этом файле описывается публичное представление пользователя. Например UserPublic с id, email, role, created_at. Важно: в схеме ответа никогда не должно быть password_hash.
"""

from pydantic import BaseModel, Field


class UserPublic(BaseModel):
    id: int
    email: str = Field(min_length=1)
    role: str
    model_config = {"from_attributes": True}
