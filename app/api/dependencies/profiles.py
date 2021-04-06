from fastapi import Path, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from app.models.orm import Profile, User
from app.resources import strings


async def get_profile_by_username_from_path(
        username: str = Path(..., min_length=1),
) -> Profile:
    profile = await Profile.get_or_none(username=username)

    if profile is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=strings.USER_DOES_NOT_EXIST_ERROR
        )
    return profile
