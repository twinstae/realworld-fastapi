from typing import Dict, Set

from app.api.dependencies.authentication import EntityDoesNotExist
from app.models.domain.users import UserInDB, User

fake_user_DB: Dict[str, UserInDB] = {}
fake_user_DB_by_username: Dict[str, UserInDB] = {}
username_set = set()

following_DB: Dict[str, Set[str]] = {}


def get_user_by_email(email) -> UserInDB:
    if email not in fake_user_DB:
        raise EntityDoesNotExist
    return fake_user_DB[email]


def get_user_by_username(username: str) -> User:
    if username in fake_user_DB_by_username:
        user_in_db: UserInDB = fake_user_DB_by_username[username]
        return User(
            username=user_in_db.username,
            email=user_in_db.email,
            bio=user_in_db.bio,
            image=user_in_db.image
        )
    raise EntityDoesNotExist


def is_user_following_for_another_user(
        target_user_name: str,
        req_user_name: str
):
    if req_user_name in following_DB:
        following_set = following_DB[req_user_name]
        if target_user_name in following_set:
            return True
    return False


def remove_user_from_followers(target_user, requested_user):
    following_DB[requested_user.username].remove(target_user.username)


async def check_username_is_taken(username: str) -> bool:
    try:
        get_user_by_username(username=username)
    except EntityDoesNotExist:
        return False
    return True


async def check_email_is_taken(email: str) -> bool:
    try:
        get_user_by_email(email=email)
    except EntityDoesNotExist:
        return False
    return True
