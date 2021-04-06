from typing import Optional, List
from pydantic.main import BaseModel
from app.models.schemas.base import ArticleBase
from app.models.orm import Article


class ArticleForResponse(ArticleBase):
    class Config:
        orm_mode = True


class ArticleInResponse(BaseModel):
    article: ArticleForResponse

    @staticmethod
    def from_article(article: Article):
        return ArticleInResponse(
            article=ArticleForResponse.from_orm(article)
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
    articles: List[ArticleForResponse]
    articles_count: int
