from pydantic.main import BaseModel

from app.models.orm import Profile
from app.models.schemas.base import ProfileBase


class ProfileInResponse(BaseModel):
    profile: ProfileBase

    @staticmethod
    def from_profile(profile: Profile, is_following: bool) -> "ProfileInResponse":
        profile_base = ProfileBase.from_profile(profile, is_following)
        return ProfileInResponse(profile=profile_base)
