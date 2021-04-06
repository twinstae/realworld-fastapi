from pydantic.main import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
