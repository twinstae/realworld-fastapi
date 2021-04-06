from typing import Optional
from pydantic.main import BaseModel
from app.models.common import DateTimeModelMixin, IDModelMixin
from app.models.orm import Profile, Article


class UserBase(BaseModel):
    username: str
    email: str


class ProfileBase(BaseModel):
    username: str
    bio: Optional[str] = None
    image: Optional[str] = None
    following: bool = False

    @staticmethod
    def from_profile(profile: Profile, is_following: bool):
        return ProfileBase(
            username=profile.username,
            bio=profile.bio,
            image=profile.image,
            following=is_following
        )


class ArticleBase(IDModelMixin, DateTimeModelMixin):
    slug: str
    title: str
    description: str
    body: str
    author: ProfileBase

    @staticmethod
    def from_entity(article: Article, is_following):
        return ArticleBase(
            slug=article.slug,
            title=article.title,
            description=article.description,
            body=article.body,
            author=ProfileBase.from_profile(article.author, is_following)
        )
