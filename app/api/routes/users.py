from fastapi import APIRouter, Depends, Body, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.api.dependencies.authentication import get_current_user_authorizer
from app.core.config import config
from app.models.domain.users import User
from app.models.schemas.users import UserInResponse, UserWithToken, UserInUpdate
from app.resources import strings
from app.services import jwt
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
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=strings.USERNAME_TAKEN,
            )

    if user_update.email and user_update.email != current_user.email:
        if await check_email_is_taken(user_update.email):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=strings.EMAIL_TAKEN,
            )
    return UserInResponse()
