from fastapi import FastAPI
from app.api.routes.api import router as api_router

API_PREFIX: str = "/api"


def get_application() -> FastAPI:
    application = FastAPI()

    application.include_router(api_router, prefix=API_PREFIX)

    return application


app = get_application()
