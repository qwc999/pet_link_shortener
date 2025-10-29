from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.click import ClickDAO
from app.dao.link import LinkDAO


class ClickService:
    def __init__(self, db: AsyncSession):
        self.click_dao = ClickDAO(db)
        self.link_dao = LinkDAO(db)

    async def register_click(self, link_id: int, click_data: dict):
        click_data["link_id"] = link_id
        return await self.click_dao.create_click(click_data)

    async def get_clicks_by_link_id(self, link_id: int, user_id: int):
        link = await self.link_dao.get_link_by_link_id(link_id)
        if not link or link.owner_id != user_id:
            return None
        return await self.click_dao.get_clicks_by_link_id(link_id)
