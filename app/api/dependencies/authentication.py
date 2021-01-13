from typing import Callable, Optional

from fastapi import Security, HTTPException, requests, Depends
from fastapi.security import APIKeyHeader
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routes.authentication import fake_user_DB_by_username
from app.core.config import JWT_TOKEN_PREFIX, SECRET_KEY
from app.models.domain.users import User, UserInDB
from app.resources import strings
from app.services import jwt

HEADER_KEY = "Authorization"


class RWAPIKeyHeader(APIKeyHeader):
    async def __call__(  # noqa: WPS610
            self,
            request: requests.Request,
    ) -> Optional[str]:
        try:
            return await super().__call__(request)
        except StarletteHTTPException as original_auth_exc:
            raise HTTPException(
                status_code=original_auth_exc.status_code,
                detail=strings.AUTHENTICATION_REQUIRED,
            )


def get_current_user_authorizer(*, required: bool = True) -> Callable:  # type: ignore
    return _get_current_user if required else _get_current_user_optional


def _get_authorization_header_retriever(
        *,
        required: bool = True,
) -> Callable:  # type: ignore
    return _get_authorization_header if required else _get_authorization_header_optional


class EntityDoesNotExist(Exception):
    pass


def get_user_by_username(username: str) -> User:
    if username in fake_user_DB_by_username:
        user_in_db: UserInDB = fake_user_DB_by_username[username]
        return User(
            username=user_in_db.username,
            email=user_in_db.email,
            bio=user_in_db.bio,
            image=user_in_db.image
        )
    raise EntityDoesNotExist


async def _get_current_user(
        token: str = Depends(_get_authorization_header_retriever()),
) -> User:
    try:
        username = jwt.get_username_from_token(token, str(SECRET_KEY))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.MALFORMED_PAYLOAD,
        )
    try:
        return get_user_by_username(username=username)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.MALFORMED_PAYLOAD,
        )


async def _get_current_user_optional(
        token: str = Depends(_get_authorization_header_retriever(required=False)),
) -> Optional[User]:
    if token:
        return await _get_current_user(token)
    return None


def _get_authorization_header(
        api_key: str = Security(RWAPIKeyHeader(name=HEADER_KEY)),
) -> str:
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.WRONG_TOKEN_PREFIX,
        )

    if token_prefix != JWT_TOKEN_PREFIX:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.WRONG_TOKEN_PREFIX,
        )

    return token


def _get_authorization_header_optional(
        authorization: Optional[str] = Security(
            RWAPIKeyHeader(name=HEADER_KEY, auto_error=False),
        ),
) -> str:
    if authorization:
        return _get_authorization_header(authorization)

    return ""
