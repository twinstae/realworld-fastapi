from fastapi import APIRouter, Depends, Body
from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.errors.exceptions import HTTP_400_BAD_REQUEST_Exception
from app.models.schemas.base import UserBase
from app.models.orm.user import User
from app.models.schemas.users import UserInResponse, UserInUpdate
from app.resources import strings
from app.services.authentication import check_username_is_taken, check_email_is_taken

router = APIRouter()
PREFIX = "Users:"


@router.get(
    "api/user",
    response_model=UserInResponse,
    name=PREFIX + "get-current-user"
)
async def retrieve_current_user(
        user: UserBase = Depends(get_current_user_authorizer())
) -> UserInResponse:
    return UserInResponse.from_user(user)


@router.put(
    "/api/user",
    response_model=UserInResponse,
    name=PREFIX + "update-current-user"
)
async def update_current_user(
        user_update: UserInUpdate = Body(..., embed=True, alias="user"),
        current_user: User = Depends(get_current_user_authorizer()),
) -> UserInResponse:
    if user_update.username and user_update.username != current_user.username:
        if await check_username_is_taken(user_update.username):
            raise HTTP_400_BAD_REQUEST_Exception(strings.USERNAME_TAKEN)

    if user_update.email and user_update.email != current_user.email:
        if await check_email_is_taken(user_update.email):
            raise HTTP_400_BAD_REQUEST_Exception(strings.EMAIL_TAKEN)

    user = update_user(current_user, user_update)
    return UserInResponse.from_user(user)


async def update_user(current_user: User, user_update: UserInUpdate) -> User:
    await current_user.update_from_dict(user_update.dict())
    return current_user
