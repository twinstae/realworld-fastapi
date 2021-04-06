from typing import Callable

from fastapi import FastAPI
from loguru import logger
from tortoise import Tortoise
from app.core.config import DATABASE_URL


def create_start_app_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await Tortoise.init(
            db_url=DATABASE_URL,
            modules={'models': ['app.models.orm']}
        )
        await Tortoise.generate_schemas()

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:
    @logger.catch
    async def stop_app() -> None:
        await Tortoise.close_connections()
    return stop_app
