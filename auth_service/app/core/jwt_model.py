from pydantic import BaseModel


class JwtPayload(BaseModel):
    sub: str
    type: str
    role: str
    iat: int
    exp: int
