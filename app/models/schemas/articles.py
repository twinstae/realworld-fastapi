from typing import Optional, List
from pydantic.main import BaseModel
from app.models.schemas.base import ArticleBase
from app.models.orm import Article, Profile


class ArticleInResponse(BaseModel):
    article: ArticleBase

    @staticmethod
    async def from_article(article: Article, current_profile: Optional[Profile], favorite=None):
        is_following = False
        if current_profile and current_profile.id != article.author.id:
            is_following = await current_profile.is_following(article.author)

        if favorite is None:
            if current_profile:
                favorite = await current_profile.have_favorited(article)
            else:
                favorite = False

        return ArticleInResponse(
            article=ArticleBase.from_entity(article, is_following, favorite)
        )


class ListOfArticlesInResponse(BaseModel):
    articles: List[ArticleBase]
    articles_count: int


class ArticleInCreate(BaseModel):
    title: str
    description: str
    body: str


class ArticleInUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None
