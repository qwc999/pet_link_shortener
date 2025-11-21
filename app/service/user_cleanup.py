from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.click import ClickDAO
from app.dao.link import LinkDAO
from app.schemas.link import LinkResponse
from app.service.link_redis import LinkRedisService


class UserCleanupService:
    def __init__(self, db: AsyncSession):
        self.link_dao = LinkDAO(db)
        self.click_dao = ClickDAO(db)
        self.link_redis = LinkRedisService()

    async def cleanup_user_data(self, user_id: int):
        user_links = await self.link_dao.get_user_links(user_id)
        for link in user_links:
            await self.click_dao.delete_clicks_by_link_id(link.id)
            await self.link_redis.invalidate_link(LinkResponse.model_validate(link))
        await self.link_dao.delete_links_by_user_id(user_id)

