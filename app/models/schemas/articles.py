from typing import Optional, List
from pydantic.main import BaseModel
from app.models.schemas.base import ArticleBase
from app.models.orm import Article


class ArticleInResponse(BaseModel):
    article: ArticleBase

    @staticmethod
    def from_article(article: Article, is_following: bool):
        return ArticleInResponse(
            article=ArticleBase.from_entity(article, is_following)
        )


class ArticleInCreate(BaseModel):
    title: str
    description: str
    body: str


class ArticleInUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None


class ListOfArticlesInResponse(BaseModel):
    articles: List[ArticleBase]
    articles_count: int
