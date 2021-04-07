from typing import Optional

from fastapi import APIRouter, Depends

from app.api.dependencies.authentication import get_current_profile, get_current_profile_optional
from app.api.dependencies.profiles import get_profile_by_username_from_path
from app.api.errors.exceptions import HTTP_400_BAD_REQUEST_Exception
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
    current_profile: Optional[Profile] = Depends(get_current_profile_optional)
) -> ProfileInResponse:
    is_following = False
    if current_profile is not None:
        is_following = await current_profile.is_following(target_profile)
    return ProfileInResponse.from_profile(
        target_profile, is_following
    )


@router.post(
    "/{username}/follow",
    response_model=ProfileInResponse,
    name=PREFIX + "follow-profile"
)
async def follow_profile(
        target_profile: Profile = Depends(get_profile_by_username_from_path),
        current_profile: Profile = Depends(get_current_profile)
) -> ProfileInResponse:
    if current_profile == target_profile:
        raise HTTP_400_BAD_REQUEST_Exception(strings.UNABLE_TO_FOLLOW_YOURSELF)

    if await current_profile.is_following(target_profile):
        raise HTTP_400_BAD_REQUEST_Exception(strings.USER_IS_ALREADY_FOLLOWED)

    await current_profile.followings.add(target_profile)

    return ProfileInResponse.from_profile(target_profile, is_following=True)


@router.delete(
    "/{username}/follow",
    response_model=ProfileInResponse,
    name=PREFIX + "unfollow-profile"
)
async def unfollow_profile(
        target_profile: Profile = Depends(get_profile_by_username_from_path),
        current_profile: Profile = Depends(get_current_profile),
) -> ProfileInResponse:
    if target_profile == current_profile:
        raise HTTP_400_BAD_REQUEST_Exception(strings.UNABLE_TO_FOLLOW_YOURSELF)

    if not await current_profile.is_following(target_profile):
        raise HTTP_400_BAD_REQUEST_Exception(strings.USER_IS_ALREADY_UNFOLLOWED)

    await current_profile.followings.remove(target_profile)

    return ProfileInResponse.from_profile(target_profile, is_following=False)
