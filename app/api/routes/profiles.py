from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.api.dependencies.authentication import get_current_profile
from app.api.dependencies.profiles import get_profile_by_username_from_path
from app.models.orm import Profile
from app.models.schemas.profile import ProfileInResponse
from app.resources import strings

router = APIRouter()
PREFIX = "profiles:"


@router.get(
    "/{username}",
    response_model=ProfileInResponse,
    name=PREFIX + "get-profile"
)
async def retrieve_profile_by_username(
    target_profile: Profile = Depends(get_profile_by_username_from_path),
    current_profile: Profile = Depends(get_current_profile)
) -> ProfileInResponse:
    return ProfileInResponse.from_profile(
        target_profile,
        is_following=await current_profile.is_following(target_profile)
    )


@router.post(
    "/{username}follow",
    response_model=ProfileInResponse,
    name=PREFIX + "follow-profile"
)
async def follow_user(
        target_profile: Profile = Depends(get_profile_by_username_from_path),
        current_profile: Profile = Depends(get_current_profile)
) -> ProfileInResponse:
    if current_profile == target_profile:
        raise bad_request_exception(strings.UNABLE_TO_FOLLOW_YOURSELF)

    if await current_profile.is_following(target_profile):
        raise bad_request_exception(strings.USER_IS_ALREADY_FOLLOWED)

    current_profile.followings.add(target_profile)

    return ProfileInResponse.from_profile(target_profile, is_following=True)


def bad_request_exception(detail: str) -> HTTPException:
    return HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail=detail
    )


@router.delete(
    "/{username}/follow",
    response_model=ProfileInResponse,
    name=PREFIX + "unsubscribe-from-user"
)
async def unsubscribe_from_user(
        target_profile: Profile = Depends(get_profile_by_username_from_path),
        current_profile: Profile = Depends(get_current_profile),
) -> ProfileInResponse:
    if target_profile == current_profile:
        raise bad_request_exception(strings.UNABLE_TO_FOLLOW_YOURSELF)

    if not await current_profile.is_following(target_profile):
        raise bad_request_exception(strings.USER_IS_ALREADY_UNFOLLOWED)

    current_profile.followings.remove(target_profile)

    return ProfileInResponse.from_profile(target_profile, is_following=False)
