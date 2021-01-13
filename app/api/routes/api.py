from fastapi import APIRouter

from app.api.routes.articles import api as articles
from app.api.routes import authentication

router = APIRouter()
router.include_router(articles.router, tags=["articles"])
router.include_router(authentication.router, tags=["authentications"], prefix="/users")
