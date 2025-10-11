from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.link import Link


class LinkDAO:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_link(self, link_dict):
        link = Link(**link_dict)
        self.db.add(link)
        await self.db.commit()
        await self.db.refresh(link)
        return link


    async def get_user_links(self, user_id):
        result = await self.db.execute(
            select(Link).where(Link.owner_id == user_id)
        )
        links = result.scalars().all()
        return links

    async def get_link_by_link_id(self, link_id):
        result = await self.db.execute(
            select(Link).where(Link.id == link_id)
        )
        return result.scalar_one_or_none()

    async def deactivate(self, link_id):
        return await self.update(link_id, {"is_active": False})

    async def update(self, link_id, update_data):
        await self.db.execute(
            update(Link).where(Link.id == link_id).values(**update_data)
        )
        await self.db.commit()
        return await self.get_link_by_link_id(link_id)
