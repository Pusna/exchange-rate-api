from pydantic import BaseModel, EmailStr


class AuthUserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr


class TokenData(BaseModel):
    email: str | None = None