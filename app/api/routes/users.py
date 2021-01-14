from fastapi import APIRouter, Depends, Body

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.routes.authentication import fake_user_DB, fake_user_DB_by_username, get_user_in_response
from app.api.routes.profiles import bad_request_exception
from app.models.domain.users import User, UserInDB
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
        user: User = Depends(get_current_user_authorizer())
) -> UserInResponse:
    return get_user_in_response(user)


def update_user(current_user: User, user_update: UserInUpdate) -> User:
    user = fake_user_DB[current_user.email]
    new_user = UserInDB(
        username=user_update.username or user.username,
        email=user_update.email or user.email,
        bio=user_update.bio or user.bio,
        image=user_update.image or user.image,
        salt=user.salt,
        hashed_password=user.hashed_password,
    )
    del fake_user_DB[user.email]
    fake_user_DB[new_user.email] = new_user
    del fake_user_DB_by_username[user.username]
    fake_user_DB_by_username[new_user.username] = new_user
    return new_user


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
            raise bad_request_exception(strings.USERNAME_TAKEN)

    if user_update.email and user_update.email != current_user.email:
        if await check_email_is_taken(user_update.email):
            raise bad_request_exception(strings.EMAIL_TAKEN)

    user = update_user(current_user, user_update)

    return get_user_in_response(user)
