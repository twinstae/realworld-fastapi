from typing import List
from fastapi import APIRouter, Body, HTTPException
from starlette import status
from starlette.status import HTTP_404_NOT_FOUND

from app.api.routes.profiles import bad_request_exception
from app.models.orm.article import Article
from app.models.schemas.articles import ArticleInResponse, ArticleInCreate, ArticleInUpdate, ListOfArticlesInResponse, \
    ArticleForResponse
from app.resources import strings
from app.services.articles import get_slug_for_article

router: APIRouter = APIRouter()

PREFIX: str = "articles:"


@router.get(
    "",
    response_model=ListOfArticlesInResponse,
    name=PREFIX + "list-articles"
)
async def list_articles() -> ListOfArticlesInResponse:
    articles: List[Article] = await Article.all()

    return ListOfArticlesInResponse(
        articles=[ArticleForResponse.from_orm(a) for a in articles],
        articles_count=len(articles)
    )


@router.get(
    "/{slug}",
    response_model=ArticleInResponse,
    name=PREFIX + "get-article"
)
async def retrieve_article_by_slug(
        slug: str
) -> ArticleInResponse:
    article = await get_article_by_slug_or_404(slug)
    return ArticleInResponse.from_article(article)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ArticleInResponse,
    name=PREFIX + "create-article"
)
async def create_new_article(
        article_create: ArticleInCreate = Body(..., embed=True, alias="article")
) -> ArticleInResponse:
    slug: str = get_slug_for_article(article_create.title)

    if await Article.exists(slug=slug):
        raise bad_request_exception(strings.WRONG_SLUG_NO_ARTICLE)

    article = await Article.create(
        slug=slug,
        title=article_create.title,
        description=article_create.description,
        body=article_create.body
    )

    return ArticleInResponse.from_article(article)


@router.put(
    "/{slug}",
    response_model=ArticleInResponse,
    name=PREFIX + "update-article",
)
async def update_article_by_slug(
        article_update: ArticleInUpdate,
        slug: str
) -> ArticleInResponse:
    article = await get_article_by_slug_or_404(slug)
    await article.update_from_dict(article_update.dict())
    return ArticleInResponse.from_article(article)


@router.delete(
    "/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
    name=PREFIX + "delete-article"
)
async def delete_by_slug(
        slug: str
) -> None:
    article = await get_article_by_slug_or_404(slug)
    await article.delete()


async def get_article_by_slug_or_404(slug):
    article = await Article.get_or_none(slug=slug)
    if article is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=strings.WRONG_SLUG_NO_ARTICLE
        )
    return article
