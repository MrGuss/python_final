from pydantic import BaseModel, Field


class UserPublic(BaseModel):
    id: int
    email: str = Field(min_length=1)
    role: str
    model_config = {"from_attributes": True}  # pyright: ignore[reportUnannotatedClassAttribute]
