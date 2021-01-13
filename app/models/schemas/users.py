from pydantic import EmailStr
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
