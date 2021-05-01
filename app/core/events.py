from app.models.orm.user import User
from typing import Callable

from fastapi import FastAPI
from loguru import logger
from tortoise import Tortoise
from app.core.config import DATABASE_URL, IS_TEST

def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await Tortoise.init(
            db_url=DATABASE_URL,
            modules={'app': ['app.models.orm']}
        )
        await Tortoise.generate_schemas()

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    
    @logger.catch
    async def stop_app() -> None:
        if IS_TEST:
            await User.all().delete()

        await Tortoise.close_connections()
    return stop_app
