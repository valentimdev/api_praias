from typing import Optional, Annotated
from pydantic import BaseModel, StringConstraints


class UserBase(BaseModel):
    username: Annotated[str, StringConstraints(min_length=1, max_length=50)]


class UserInDB(UserBase):
    id: int
    hashed_password: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserLogin(UserBase):
    password: str


class UserOut(UserBase):
    id: int


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str
