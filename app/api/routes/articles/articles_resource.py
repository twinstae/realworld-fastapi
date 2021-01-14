from typing import Dict, List

from fastapi import APIRouter, Body, HTTPException
from starlette import status
from starlette.status import HTTP_400_BAD_REQUEST

from app.models.domain.articles import Article
from app.models.schemas.articles import ArticleInResponse, ArticleInCreate, ArticleInUpdate, ListOfArticlesInResponse, \
    ArticleForResponse
from app.resources import strings
from app.services.articles import get_slug_for_article

fake_db: Dict[str, Article] = {}

router: APIRouter = APIRouter()

PREFIX: str = "articles:"


@router.get(
    "",
    response_model=ListOfArticlesInResponse,
    name=PREFIX + "list-articles"
)
async def list_articles() -> ListOfArticlesInResponse:
    articles: List[Article] = list(fake_db.values())[-10:]

    return ListOfArticlesInResponse(
        articles=[
            get_article_for_response(a)
            for a in articles
        ],
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
    check_article_for_slug(slug)
    return get_article_in_response(fake_db[slug])


def get_article_for_response(article: Article) -> ArticleForResponse:
    return ArticleForResponse(
        title=article.title,
        description=article.description,
        body=article.body,
        slug=article.slug,
        created_at=article.created_at,
        updated_at=article.updated_at
    )


def get_article_in_response(article: Article) -> ArticleInResponse:
    return ArticleInResponse(
        article=get_article_for_response(article=article)
    )


def check_article_for_slug(slug) -> None:
    if slug not in fake_db:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.WRONG_SLUG_NO_ARTICLE
        )


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
    check_article_for_slug(slug)

    fake_db[slug] = Article(
        slug=slug,
        title=article_create.title,
        description=article_create.description,
        body=article_create.body
    )

    return get_article_in_response(fake_db[slug])


@router.put(
    "/{slug}",
    response_model=ArticleInResponse,
    name=PREFIX + "update-article",
)
async def update_article_by_slug(
        article_update: ArticleInUpdate,
        slug: str
) -> ArticleInResponse:
    check_article_for_slug(slug)

    article: Article = fake_db[slug]
    article.title = article_update.title or article.title
    article.description = article_update.description or article.description
    article.body = article_update.body or article.body
    fake_db[slug] = article

    return get_article_in_response(fake_db[slug])


@router.delete(
    "/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
    name=PREFIX + "delete-article"
)
async def delete_by_slug(
        slug: str
) -> None:
    check_article_for_slug(slug)
    del fake_db[slug]
