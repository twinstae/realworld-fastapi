from app.api.dependencies.authentication import get_user_by_username, EntityDoesNotExist
from app.api.routes.authentication import get_user_by_email


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
