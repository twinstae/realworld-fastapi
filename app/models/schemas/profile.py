from pydantic.main import BaseModel

from app.models.orm import Profile
from app.models.schemas.base import ProfileBase


class ProfileInResponse(BaseModel):
    profile: ProfileBase

    @staticmethod
    def from_profile(profile: Profile, is_following: bool):
        ProfileInResponse(profile=ProfileBase(
            username=profile.username,
            bio=profile.bio,
            image=profile.image,
            following=is_following
        ))