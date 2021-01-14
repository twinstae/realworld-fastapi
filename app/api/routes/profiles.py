from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.api.dependencies.authentication import get_current_user_authorizer
from app.api.dependencies.profiles import get_profile_by_username_from_path
from app.models.domain.profiles import Profile
from app.models.domain.users import User
from app.models.schemas.profile import ProfileInResponse
from app.resources import strings
from app.services.authentication import following_DB, remove_user_from_followers

router = APIRouter()
PREFIX = "profiles:"


@router.get(
    "/{username}",
    response_model=ProfileInResponse,
    name=PREFIX + "get-profile"
)
async def retrieve_profile_by_username(
        profile: Profile = Depends(get_profile_by_username_from_path),
) -> ProfileInResponse:
    return ProfileInResponse(profile=profile)


def add_user_into_followers(target_user, requested_user):
    following_DB[requested_user.username].add(target_user.username)


@router.post(
    "/{username}follow",
    response_model=ProfileInResponse,
    name=PREFIX + "follow-user"
)
async def follow_for_user(
        profile: Profile = Depends(get_profile_by_username_from_path),
        user: User = Depends(get_current_user_authorizer()),
) -> ProfileInResponse:
    if user.username == profile.username:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.UNABLE_TO_FOLLOW_YOURSELF
        )

    if profile.following:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.USER_IS_ALREADY_FOLLOWED
        )

    add_user_into_followers(
        target_user=profile,
        requested_user=user
    )

    return ProfileInResponse(
        profile=profile.copy(update={"following": True})
    )


@router.delete(
    "/{username}/follow",
    response_model=ProfileInResponse,
    name=PREFIX + "unsubscribe-from-user"
)
async def unsubscribe_from_user(
        profile: Profile = Depends(get_profile_by_username_from_path),
        user: User = Depends(get_current_user_authorizer()),
) -> ProfileInResponse:
    if user.username == profile.username:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.UNABLE_TO_FOLLOW_YOURSELF
        )

    if not profile.following:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.USER_IS_ALREADY_UNFOLLOWED
        )

    remove_user_from_followers(
        target_user=profile,
        requested_user=user
    )

    return ProfileInResponse(
        profile=profile.copy(update={"following": False})
    )
