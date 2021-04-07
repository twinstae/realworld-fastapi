from fastapi import APIRouter, Depends

from app.api.dependencies.authentication import get_current_profile
from app.api.errors.exceptions import HTTP_400_BAD_REQUEST_Exception
from app.models.orm import Article, Profile
from app.models.schemas.articles import ArticleInResponse
from app.resources import strings
from app.services.articles import get_article_by_slug_from_path

router = APIRouter()


@router.post(
    "/{slug}/favorite",
    response_model=ArticleInResponse,
    name="articles:favorite-article",
)
async def favorite_article(
        article: Article = Depends(get_article_by_slug_from_path),
        current_profile: Profile = Depends(get_current_profile),
) -> ArticleInResponse:
    if await current_profile.have_favorited(article):
        raise HTTP_400_BAD_REQUEST_Exception(strings.ARTICLE_IS_ALREADY_FAVORITED)

    await current_profile.favorite(article)

    return await ArticleInResponse.from_article(article, current_profile, True)


@router.delete(
    "/{slug}/favorite",
    response_model=ArticleInResponse,
    name="articles:unfavorite-article",
)
async def unfavorite_article(
    article: Article = Depends(get_article_by_slug_from_path),
    current_profile: Profile = Depends(get_current_profile),
) -> ArticleInResponse:
    if not await current_profile.have_favorited(article):
        raise HTTP_400_BAD_REQUEST_Exception(strings.ARTICLE_IS_NOT_FAVORITED)

    await current_profile.unfavorite(article)
    return await ArticleInResponse.from_article(article, current_profile, False)
