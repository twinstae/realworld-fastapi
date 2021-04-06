from typing import Optional
from pydantic.main import BaseModel
from app.models.common import DateTimeModelMixin, IDModelMixin


class ArticleBase(IDModelMixin, DateTimeModelMixin):
    slug: str
    title: str
    description: str
    body: str


class UserBase(BaseModel):
    username: str
    email: str


class ProfileBase(BaseModel):
    username: str
    bio: Optional[str] = None
    image: Optional[str] = None
    following: bool = False
