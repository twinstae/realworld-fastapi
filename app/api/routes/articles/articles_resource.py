from typing import List, Type
from fastapi import APIRouter, Body, HTTPException, Depends
from pypika import Table
from starlette import status
from starlette.status import HTTP_404_NOT_FOUND
from tortoise.functions import Function
from app.api.dependencies.authentication import get_current_profile
from app.api.routes.profiles import bad_request_exception
from app.models.orm import Profile
from app.models.orm.article import Article
from app.models.schemas.articles import ArticleInResponse, ArticleInCreate, ArticleInUpdate, ListOfArticlesInResponse
from app.models.schemas.base import ArticleBase
from app.resources import strings
from app.services.articles import get_slug_for_article
from tortoise.models import Model

router: APIRouter = APIRouter()

PREFIX: str = "articles:"


@router.get(
    "",
    response_model=ListOfArticlesInResponse,
    name=PREFIX + "list-articles"
)
async def list_articles() -> ListOfArticlesInResponse:
    articles: List[Article] = await Article.all().prefetch_related("author")

    return ListOfArticlesInResponse(
        articles=[ArticleBase.from_entity(a, False) for a in articles],
        articles_count=len(articles)
    )


@router.get(
    "/{slug}",
    response_model=ArticleInResponse,
    name=PREFIX + "get-article"
)
async def retrieve_article_by_slug(
    slug: str,
    current_profile: Profile = Depends(get_current_profile())
) -> ArticleInResponse:
    article = await get_article_by_slug_or_404(slug)
    isFollowing = await current_profile.is_following(article.author)
    return ArticleInResponse.from_article(article, isFollowing)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ArticleInResponse,
    name=PREFIX + "create-article"
)
async def create_new_article(
        article_create: ArticleInCreate = Body(..., embed=True, alias="article"),
        current_profile: Profile = Depends(get_current_profile())
) -> ArticleInResponse:
    slug: str = get_slug_for_article(article_create.title)

    if await Article.exists(slug=slug):
        raise bad_request_exception(strings.WRONG_SLUG_NO_ARTICLE)

    article = await Article.create(
        slug=slug,
        title=article_create.title,
        description=article_create.description,
        body=article_create.body,
        author=current_profile
    )
    return ArticleInResponse.from_article(article, False)


@router.put(
    "/{slug}",
    response_model=ArticleInResponse,
    name=PREFIX + "update-article",
)
async def update_article_by_slug(
        article_update: ArticleInUpdate,
        slug: str,
        current_profile: Profile = Depends(get_current_profile())
) -> ArticleInResponse:
    article = await get_article_by_slug_or_404(slug)

    if article.author is not current_profile:
        raise bad_request_exception("You can modify only your article")

    await article.update_from_dict(article_update.dict())
    return ArticleInResponse.from_article(article, False)


@router.delete(
    "/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
    name=PREFIX + "delete-article"
)
async def delete_by_slug(
    slug: str,
    current_profile: Profile = Depends(get_current_profile())
) -> None:
    article = await get_article_by_slug_or_404(slug)
    if article.author is not current_profile:
        raise bad_request_exception("You can delete only your article")
    await article.delete()


async def get_article_by_slug_or_404(slug) -> Article:
    article = await Article.get_or_none(slug=slug).prefetch_related("author")
    if article is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=strings.WRONG_SLUG_NO_ARTICLE
        )
    return article
