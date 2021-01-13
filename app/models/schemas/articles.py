from typing import Optional, List

from pydantic.main import BaseModel

from app.models.domain.articles import Article


class ArticleForResponse(Article):
    pass


class ArticleInResponse(BaseModel):
    article: ArticleForResponse


class ArticleInCreate(BaseModel):
    title: str
    description: str
    body: str


class ArticleInUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None


class ListOfArticlesInResponse(BaseModel):
    articles: List[ArticleForResponse]
    articles_count: int
