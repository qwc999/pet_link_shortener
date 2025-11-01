from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.user import UserDAO
from app.schemas.user import UserCreate, UserResponse, UserLogin, UserUpdate
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

    async def authenticate_user(self, user_data: UserLogin) -> UserResponse | None:
        user = await self.user_dao.get_user_by_email(user_data.email)
        if not user:
            return None
        if not user.is_active:
            return None
        if not verify_password(user_data.password, user.password):
            return None
        return UserResponse.model_validate(user)

    async def get_user_by_user_id_for_auth(self, user_id: int):
        return await self.user_dao.get_user_by_id(user_id)

    async def deactivate_user(self, user_id: int) -> UserResponse | None:
        deleted_user = await self.user_dao.deactivate_user(user_id)
        if not deleted_user:
            return None
        return UserResponse.model_validate(deleted_user)

    async def update_user(self, user_id: int, data: UserUpdate) -> UserResponse | None:
        update_dict = data.model_dump(exclude_unset=True)   # удаляет None
        if "password" in update_dict:
            update_dict["password"] = get_hash(update_dict["password"])
        if "email" in update_dict:
            user_exists = await self.user_dao.get_user_by_email(update_dict["email"])
            if user_exists and user_exists.id != user_id:
                raise ValueError("Email already taken")
        updated_user = await self.user_dao.update(user_id, update_dict)
        if not updated_user:
            return None
        return UserResponse.model_validate(updated_user)
