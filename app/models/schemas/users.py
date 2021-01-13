from typing import Optional

from pydantic import EmailStr, HttpUrl
from pydantic.main import BaseModel

from app.models.domain.users import User


class UserInLogin(BaseModel):
    email: EmailStr
    password: str


class UserInCreate(UserInLogin):
    username: str


class UserWithToken(User):
    token: str


class UserInResponse(BaseModel):
    user: UserWithToken


class UserInUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[HttpUrl] = None
