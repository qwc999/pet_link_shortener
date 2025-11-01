from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class UserDAO:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create_user(self, data: dict) -> User:
        user = User(**data)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update(self, user_id, update_data) -> User | None:
        await self.db.execute(
            update(User).where(User.id == user_id).values(**update_data)
        )
        await self.db.commit()
        return await self.get_user_by_id(user_id)

    async def get_user_by_id(self, user_id) -> User | None:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def deactivate_user(self, user_id) -> User | None:
        return await self.update(user_id, {"is_active": False})
