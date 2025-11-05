import secrets
import string
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.link import LinkDAO
from app.schemas.link import LinkResponse, LinkCreate
from app.service.link_redis import LinkRedisService


class LinkService:
    def __init__(self, db: AsyncSession):
        self.link_dao = LinkDAO(db)
        self.link_redis = LinkRedisService()

    @staticmethod
    def _generate_short_code(length: int = 6) -> str:
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    async def create_link(self, link_data: LinkCreate, current_user_id: int) -> LinkResponse:
        max_attempts = 10
        for i in range(max_attempts):
            short_code = self._generate_short_code()
            data = {"original_url": str(link_data.original_url),
                    "short_code": short_code,
                    "owner_id": current_user_id}
            exists = await self.get_link_for_redirect(short_code)
            if exists:
                continue
            result = await self.link_dao.create_link(data)
            result = LinkResponse.model_validate(result)
            await self.link_redis.set_link(result)
            return result
        raise ValueError("Unexpected error, try again")

    async def get_user_links(self, current_user_id: int) -> list[LinkResponse]:
        result = await self.link_dao.get_user_links(current_user_id)
        return [LinkResponse.model_validate(link) for link in result]

    async def delete_link(self, link_id: int, current_user_id: int) -> LinkResponse | None:
        link_data = await self.link_dao.get_link_by_link_id(link_id)
        if link_data and link_data.owner_id == current_user_id:
            new_link_data = await self.link_dao.deactivate(link_id)
            result = LinkResponse.model_validate(new_link_data)
            await self.link_redis.invalidate_link(result)
            return result
        else:
            return None

    async def get_link_by_id(self, link_id: int, current_user_id: int) -> LinkResponse | None:
        link_data = await self.link_dao.get_link_by_link_id(link_id)
        if link_data and link_data.owner_id == current_user_id:
            return LinkResponse.model_validate(link_data)
        return None

    async def get_link_for_redirect(self, short_code: str) -> LinkResponse | None:
        link_from_cache = await self.link_redis.get_link_by_short_code(short_code)
        if link_from_cache:
            return LinkResponse.model_validate(link_from_cache)
        link = await self.link_dao.get_link_for_redirect(short_code)
        if link:
            link_data = LinkResponse.model_validate(link)
            await self.link_redis.set_link(link_data)
            return link_data
        return None
