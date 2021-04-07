from typing import List, Optional
from fastapi import APIRouter, Body, Depends, Query
from starlette import status
from app.api.dependencies.authentication import get_current_profile
from app.api.errors.exceptions import HTTP_400_BAD_REQUEST_Exception
from app.models.orm import Profile
from app.models.orm.article import Article
from app.models.schemas.articles import ArticleInResponse, ArticleInCreate, ArticleInUpdate, ListOfArticlesInResponse
from app.models.schemas.base import ArticleBase
from app.resources import strings
from app.services.articles import get_slug_for_article, get_article_by_slug_from_path
from app.api.dependencies.authentication import get_current_profile_optional
router: APIRouter = APIRouter()

PREFIX: str = "articles:"


@router.get(
    "",
    response_model=ListOfArticlesInResponse,
    name=PREFIX + "list-articles"
)
async def list_articles(
        author: str = Query(None, max_length=16),
        favorited: str = Query(None, max_length=16),
        limit: int = Query(20),
        offset: int = Query(0),
) -> ListOfArticlesInResponse:
    query = Article.all().prefetch_related("author")

    if author is not None:
        query = query.filter(author__username=author)
    if favorited is not None:
        query = query.filter(favorited__username=favorited)

    articles: List[Article] = await query.offset(offset).limit(limit)
    articles_count = await query.count()

    return ListOfArticlesInResponse(
        articles=[ArticleBase.from_entity(a, False) for a in articles],
        articles_count=articles_count
    )


@router.get(
    "/{slug}",
    response_model=ArticleInResponse,
    name=PREFIX + "get-article"
)
async def retrieve_article_by_slug(
    article: Article = Depends(get_article_by_slug_from_path),
    current_profile: Optional[Profile] = Depends(get_current_profile_optional)
) -> ArticleInResponse:
    return await ArticleInResponse.from_article(article, current_profile)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ArticleInResponse,
    name=PREFIX + "create-article"
)
async def create_new_article(
        article_create: ArticleInCreate = Body(..., embed=True, alias="article"),
        current_profile: Profile = Depends(get_current_profile)
) -> ArticleInResponse:
    slug: str = get_slug_for_article(article_create.title)

    if await Article.exists(slug=slug):
        raise HTTP_400_BAD_REQUEST_Exception(strings.WRONG_SLUG_NO_ARTICLE)

    article = await Article.create(
        slug=slug,
        title=article_create.title,
        description=article_create.description,
        body=article_create.body,
        author=current_profile
    )
    return await ArticleInResponse.from_article(article, current_profile)


@router.put(
    "/{slug}",
    response_model=ArticleInResponse,
    name=PREFIX + "update-article",
)
async def update_article_by_slug(
        article: Article = Depends(get_article_by_slug_from_path),
        article_update: ArticleInUpdate = Body(..., embed=True, alias="article"),
        current_profile: Profile = Depends(get_current_profile)
) -> ArticleInResponse:
    if article.author.id is not current_profile.id:
        raise HTTP_400_BAD_REQUEST_Exception("You can modify only your article")

    await article.update_from_dict(article_update.dict())
    return await ArticleInResponse.from_article(article, current_profile)


@router.delete(
    "/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
    name=PREFIX + "delete-article"
)
async def delete_by_slug(
    article: Article = Depends(get_article_by_slug_from_path),
    current_profile: Profile = Depends(get_current_profile)
) -> None:
    if article.author.id is not current_profile.id:
        raise HTTP_400_BAD_REQUEST_Exception("You can delete only your article")
    await article.delete()
