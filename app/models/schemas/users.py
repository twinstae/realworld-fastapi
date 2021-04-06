from typing import Optional

from pydantic import EmailStr, HttpUrl
from pydantic.main import BaseModel

from app.core.config import SECRET_KEY
from app.models.domain.users import UserBase
from app.services import jwt


class UserInLogin(BaseModel):
    email: EmailStr
    password: str


class UserInCreate(UserInLogin):
    username: str


class UserWithToken(UserBase):
    token: str


class UserInResponse(BaseModel):
    user: UserWithToken

    @staticmethod
    def from_user(user):
        token = jwt.create_access_token_for_username(
            user.username,
            str(SECRET_KEY)
        )
        return UserInResponse(
            user=UserWithToken(
                username=user.username,
                email=user.email,
                token=token
            )
        )


class UserInUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[HttpUrl] = None
