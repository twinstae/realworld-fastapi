from typing import Optional

from fastapi import Path, Depends, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from app.api.dependencies.authentication import get_current_user_authorizer, EntityDoesNotExist
from app.models.domain.profiles import Profile
from app.models.domain.users import User, UserInDB
from app.resources import strings
from app.services.authentication import get_user_by_username


def get_profile_by_username(
    username: str,
    requested_user: Optional[UserInDB] = None
):
    user = get_user_by_username(username=username)
    profile = Profile(
        username=user.username,
        bio=user.bio,
        image=user.image
    )
    if requested_user:
        profile.following = True

        """
        is_user_following_for_another_user(
            target_user_name=user.username,
            req_user_name=requested_user.username
        )
        """

    return profile


async def get_profile_by_username_from_path(
    username: str = Path(..., min_length=1),
    user: Optional[User] = Depends(get_current_user_authorizer(required=False)),
) -> Profile:
    try:
        return get_profile_by_username(
            username=username,
            requested_user=user
        )

    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=strings.USER_DOES_NOT_EXIST_ERROR
        )
