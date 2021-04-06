from fastapi import APIRouter

from app.api.routes import authentication, profiles, users
from app.api.routes.articles import api as articles

router = APIRouter()
router.include_router(
    articles.router,
    tags=["articles"])
router.include_router(authentication.router, tags=["authentications"], prefix="/users")
router.include_router(profiles.router, tags=["profiles"], prefix="/profiles")
router.include_router(users.router, tags=["users"], prefix="/users")
