from typing import Union

from fastapi import APIRouter, Body
from starlette.status import HTTP_201_CREATED

from app.api.routes.profiles import bad_request_exception
from app.core.config import SECRET_KEY
from app.models.domain.users import UserInDB, User
from app.models.schemas.users import UserInResponse, UserInLogin, UserWithToken, UserInCreate
from app.resources import strings
from app.services import jwt
from app.services.authentication import fake_user_DB, get_user_by_email, fake_user_DB_by_username

router: APIRouter = APIRouter()

PREFIX = "auth:"


@router.post(
    '/login',
    response_model=UserInResponse,
    name=PREFIX + "login",
)
async def login(
        user_login: UserInLogin = Body(..., embed=True, alias="user")
) -> UserInResponse:
    wrong_login_error = bad_request_exception(strings.INCORRECT_LOGIN_INPUT)
    if user_login.email not in fake_user_DB:
        raise wrong_login_error

    user = get_user_by_email(email=user_login.email)

    if not user.check_password(user_login.password):
        raise wrong_login_error

    return get_user_in_response(user)


@router.post(
    "",
    status_code=HTTP_201_CREATED,
    response_model=UserInResponse,
    name=PREFIX + "register"
)
async def register(
        user_create: UserInCreate = Body(..., embed=True, alias="user")
) -> UserInResponse:
    if user_create.username in fake_user_DB_by_username:
        raise bad_request_exception(strings.USERNAME_TAKEN)

    if user_create.email in fake_user_DB:
        raise bad_request_exception(strings.EMAIL_TAKEN)

    user: UserInDB = UserInDB(
        username=user_create.username,
        email=user_create.email
    )
    user.change_password(user_create.password)

    fake_user_DB[user_create.email] = user
    fake_user_DB_by_username[user_create.username] = user

    return get_user_in_response(user)


def get_user_in_response(user: Union[UserInDB, User]) -> UserInResponse:
    token = jwt.create_access_token_for_username(
        user.username,
        str(SECRET_KEY)
    )
    return UserInResponse(
        user=get_user_with_token(user, token)
    )


def get_user_with_token(user: Union[UserInDB, User], token: str) -> UserWithToken:
    return UserWithToken(
        username=user.username,
        email=user.email,
        bio=user.bio,
        image=user.image,
        token=token
    )
