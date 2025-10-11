from app.models.user import User


async def get_current_user():
    # todo
    return User(
        id=1,
        email="test1@example.com",
        password="123",
        is_active=True
    )
