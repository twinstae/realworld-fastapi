import random
import string

from fastapi import HTTPException, Path
from slugify import slugify
from starlette.status import HTTP_404_NOT_FOUND

from app.models.orm import Article
from app.resources import strings


def get_slug_for_article(title: str) -> str:
    return slugify(title) + ''.join(random.choice(string.ascii_lowercase) for _ in range(6))


async def get_article_by_slug_from_path(slug: str = Path(..., min_length=1)) -> Article:
    article = await Article.get_or_none(slug=slug).prefetch_related("author")
    if article is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=strings.WRONG_SLUG_NO_ARTICLE
        )
    return article
