import secrets
import string

from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.link import LinkDAO
from app.schemas.link import LinkResponse, LinkCreate, LinkDelete


class LinkService:
    def __init__(self, db: AsyncSession):
        self.link_dao = LinkDAO(db)

    def _generate_short_code(self, length: int = 6):
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    async def create_link(self, link_data: LinkCreate, current_user_id: int) -> LinkResponse:
        short_code = self._generate_short_code()
        # todo : проверка на уникальность шорт кода
        data = {"original_url": str(link_data.original_url),
                          "short_code": short_code,
                          "owner_id": current_user_id}
        result = await self.link_dao.create_link(data)
        result = LinkResponse.model_validate(result)
        return result

    async def get_user_links(self, current_user_id: int) -> list[LinkResponse]:
        result = await self.link_dao.get_user_links(current_user_id)
        return [LinkResponse.model_validate(link) for link in result]

    async def delete_link(self, link_id: int, current_user_id: int) -> LinkResponse | None:
        link_data = await self.link_dao.get_link_by_link_id(link_id)
        if link_data and link_data.owner_id == current_user_id:
            new_link_data = await self.link_dao.deactivate(link_id)
            return LinkResponse.model_validate(new_link_data)
        else:
            return None

    async def get_link_by_id(self, link_id, current_user_id):
        link_data = await self.link_dao.get_link_by_link_id(link_id)
        if link_data and link_data.owner_id == current_user_id:
            return LinkResponse.model_validate(link_data)
        else:
            return None

    async def get_link_for_redirect(self, short_code):
        return await self.link_dao.get_link_for_redirect(short_code)
