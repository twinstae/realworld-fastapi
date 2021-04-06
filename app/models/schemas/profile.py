from pydantic.main import BaseModel

from app.models.orm import Profile
from app.models.schemas.base import ProfileBase


class ProfileInResponse(BaseModel):
    profile: ProfileBase

    @staticmethod
    def from_profile(profile: Profile, is_following: bool):
        ProfileInResponse(profile=ProfileBase.from_profile(
            profile, is_following=is_following
        ))
