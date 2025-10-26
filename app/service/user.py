from enum import verify

from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.user import UserDAO
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.utils.security import get_hash, verify_password


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_dao = UserDAO(db)

    async def register_user(self, user_data: UserCreate) -> UserResponse:
        user_exists = await self.user_dao.get_user_by_email(user_data.email)
        if user_exists:
            raise ValueError("User already exists")
        hashed_password = get_hash(user_data.password)
        data = {"email": user_data.email,
                "password": hashed_password}
        result = await self.user_dao.create_user(data)
        return UserResponse.model_validate(result)

    async def authenticate_user(self, user_data: UserLogin):
        user = await self.user_dao.get_user_by_email(user_data.email)
        if not user:
            return None
        if not verify_password(user_data.password, user.password):
            return None
        return UserResponse.model_validate(user)

