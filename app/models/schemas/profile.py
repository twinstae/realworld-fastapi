from pydantic.main import BaseModel

from app.models.domain.profiles import Profile


class ProfileInResponse(BaseModel):
    profile: Profile
