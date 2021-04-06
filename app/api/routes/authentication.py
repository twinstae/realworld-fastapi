from fastapi import APIRouter, Body
from starlette.status import HTTP_201_CREATED
from app.api.routes.profiles import bad_request_exception
from app.models.orm import Profile
from app.models.orm.user import User
from app.models.schemas.users import UserInResponse, UserInLogin, UserInCreate
from app.resources import strings
from app.services.authentication import create_user_and_set_password

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
    user = await User.get_or_none(email=user_login.email)

    if not user.check_password(user_login.password):
        raise bad_request_exception(strings.INCORRECT_LOGIN_INPUT)
    return UserInResponse.from_user(user)


@router.post(
    "",
    status_code=HTTP_201_CREATED,
    response_model=UserInResponse,
    name=PREFIX + "register"
)
async def register(
        user_create: UserInCreate = Body(..., embed=True, alias="user")
) -> UserInResponse:
    if await User.exists(username=user_create.username):
        raise bad_request_exception(strings.USERNAME_TAKEN)

    if await User.exists(email=user_create.email):
        raise bad_request_exception(strings.EMAIL_TAKEN)

    user = await create_user_and_set_password(user_create)
    await Profile.create(user=user, username=user.username)
    return UserInResponse.from_user(user)
