from typing import Callable, Optional

from fastapi import Security, HTTPException, requests, Depends
from fastapi.security import APIKeyHeader
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import JWT_TOKEN_PREFIX, SECRET_KEY
from app.models.orm import Profile
from app.models.orm.user import User
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


def get_current_profile():
    current_user = await _get_current_user()
    current_profile = await Profile.get_or_none(user=current_user)
    current_profile.following = False
    return current_profile


def _get_authorization_header_retriever(
        *,
        required: bool = True,
) -> Callable:  # type: ignore
    return _get_authorization_header if required else _get_authorization_header_optional


def _get_authorization_header(
        api_key: str = Security(RWAPIKeyHeader(name=HEADER_KEY)),
) -> str:
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError:
        raise forbidden_exception(strings.WRONG_TOKEN_PREFIX)

    if token_prefix != JWT_TOKEN_PREFIX:
        raise forbidden_exception(strings.WRONG_TOKEN_PREFIX)

    return token


class EntityDoesNotExist(Exception):
    pass


def _get_authorization_header_optional(
        authorization: Optional[str] = Security(
            RWAPIKeyHeader(name=HEADER_KEY, auto_error=False),
        ),
) -> str:
    if authorization:
        return _get_authorization_header(authorization)
    return ""


async def _get_current_user(
        token: str = Depends(_get_authorization_header_retriever()),
) -> User:
    try:
        username = jwt.get_username_from_token(token, str(SECRET_KEY))
    except ValueError:
        raise forbidden_exception(strings.MALFORMED_PAYLOAD)

    user = await User.get_or_none(username=username)
    if user is None:
        raise forbidden_exception(strings.MALFORMED_PAYLOAD)
    return user


def forbidden_exception(detail: str):
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail,
    )


async def _get_current_user_optional(
        token: str = Depends(_get_authorization_header_retriever(required=False)),
) -> Optional[User]:
    if token:
        return await _get_current_user(token)
    return None
