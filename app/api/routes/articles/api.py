from fastapi import APIRouter

from app.api.routes.articles import articles_resource, articles_common

router = APIRouter()

router.include_router(articles_common.router, prefix="/articles")
router.include_router(articles_resource.router, prefix="/articles")