from typing import Dict, List

from fastapi import APIRouter, Body
from starlette import status

from app.models.domain.articles import Article
from app.models.schemas.articles import ArticleInResponse, ArticleInCreate, ArticleInUpdate, ListOfArticlesInResponse, \
    ArticleForResponse
from app.services.articles import get_slug_for_article

fake_db: Dict[str, Article] = {}

router: APIRouter = APIRouter()

prefix: str = "articles:"


@router.get(
    "",
    response_model=ListOfArticlesInResponse,
    name=prefix + "list-articles"
)
async def list_articles() -> ListOfArticlesInResponse:
    articles: List[Article] = list(fake_db.values())[-10:]

    return ListOfArticlesInResponse(
        articles=[
            ArticleForResponse(
                slug=a.slug,
                title=a.title,
                description=a.description,
                body=a.body
            ) for a in articles],
        articles_count=len(articles)
    )


@router.get(
    "/{slug}",
    response_model=ArticleInResponse,
    name=prefix + "get-article"
)
async def retrieve_article_by_slug(
        slug: str
) -> ArticleInResponse:
    return ArticleInResponse(
        article=fake_db[slug]
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ArticleInResponse,
    name=prefix + "create-article"
)
async def create_new_article(
        article_create: ArticleInCreate = Body(..., embed=True, alias="article")
) -> ArticleInResponse:
    slug: str = get_slug_for_article(article_create.title)
    fake_db[slug] = Article(
        slug=slug,
        title=article_create.title,
        description=article_create.description,
        body=article_create.body
    )

    return ArticleInResponse(article=fake_db[slug])


@router.put(
    "/{slug}",
    response_model=ArticleInResponse,
    name=prefix + "update-article",
)
async def update_article_by_slug(
        article_update: ArticleInUpdate,
        slug: str
) -> ArticleInResponse:
    article: Article = fake_db[slug]
    article.title = article_update.title or article.title
    article.description = article_update.description or article.description
    article.body = article_update.body or article.body
    fake_db[slug] = article

    return ArticleInResponse(
        article=fake_db[slug]
    )


@router.delete(
    "/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
    name=prefix + "delete-article"
)
async def delete_by_slug(
        slug: str
) -> None:
    del fake_db[slug]
