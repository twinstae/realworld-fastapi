from typing import Dict

from fastapi import APIRouter, Body, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from app.api.dependencies.authentication import EntityDoesNotExist
from app.core.config import config
from app.models.domain.users import UserInDB
from app.models.schemas.users import UserInResponse, UserInLogin, UserWithToken, UserInCreate
from app.resources import strings
from app.services import jwt

router: APIRouter = APIRouter()

PREFIX = "auth:"

fake_user_DB: Dict[str, UserInDB] = {}
fake_user_DB_by_username: Dict[str, UserInDB] = {}

username_set = set()


def get_user_by_email(email) -> UserInDB:
    if email not in fake_user_DB:
        raise EntityDoesNotExist
    return fake_user_DB[email]


@router.post(
    '/login',
    response_model=UserInResponse,
    name=PREFIX + "login",
)
async def login(
        user_login: UserInLogin = Body(..., embed=True, alias="user")
) -> UserInResponse:
    wrong_login_error = HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail=strings.INCORRECT_LOGIN_INPUT,
    )
    email: str = user_login.email
    if email not in fake_user_DB:
        raise wrong_login_error

    user = get_user_by_email(email=email)

    if not user.check_password(user_login.password, ):
        raise wrong_login_error

    token = jwt.create_access_token_for_user(user, str(config.SECRET_KEY))

    return UserInResponse(
        user=UserWithToken(
            username=user.username,
            email=user.email,
            bio=user.bio,
            image=user.image,
            token=token
        )
    )


@router.post(
    "",
    status_code=HTTP_201_CREATED,
    response_model=UserInResponse,
    name=PREFIX + "register"
)
async def register(
        user_create: UserInCreate = Body(..., embed=True, alias="user")
) -> UserInResponse:
    if user_create.username in username_set:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.USERNAME_TAKEN,
        )

    if user_create.email in fake_user_DB:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.EMAIL_TAKEN,
        )

    user: UserInDB = UserInDB(
        username=user_create.username,
        email=user_create.email
    )
    user.change_password(user_create.password)

    fake_user_DB[user_create.email] = user
    fake_user_DB_by_username[user_create.username] = user

    token = jwt.create_access_token_for_user(user, str(config.SECRET_KEY))

    return UserInResponse(
        user=UserWithToken(
            username=user.username,
            email=user.email,
            bio=user.bio,
            image=user.image,
            token=token
        )
    )
