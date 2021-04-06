from app.models.orm.user import User


async def check_username_is_taken(username: str) -> bool:
    return await User.exists(username=username)


async def check_email_is_taken(email: str) -> bool:
    return await User.exists(email=email)


async def create_user_and_set_password(user_create):
    user = User(
        username=user_create.username,
        email=user_create.email
    )
    user.change_password(user_create.password)
    await user.save()
    return user
