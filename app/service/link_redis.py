import json
from app.redis_cache import redis_cache
from app.schemas.link import LinkResponse


class LinkRedisService:
    async def set_link(self, link: LinkResponse):
        key = f"link:{link.short_code}"
        link_data = link.model_dump_json()
        await redis_cache.set(key, link_data)

    async def invalidate_link(self, link: LinkResponse):
        key = f"link:{link.short_code}"
        await redis_cache.delete(key)

    async def get_link_by_short_code(self, short_code: str) -> LinkResponse | None:
        key = f"link:{short_code}"
        result = await redis_cache.get(key)
        if result:
            result_dict = json.loads(result)
            return LinkResponse(**result_dict)
        return None
