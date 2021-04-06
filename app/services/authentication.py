from app.models.orm.user import User


async def check_username_is_taken(username: str) -> bool:
    return await User.exists(username=username)


async def check_email_is_taken(email: str) -> bool:
    return await User.exists(email=email)
