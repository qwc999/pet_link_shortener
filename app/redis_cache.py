import redis.asyncio as redis

from app.config import settings


class RedisCache:
    def __init__(self):
        self.redis_client = None

    async def init_redis(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses = True,
            encoding = "utf-8")
        await self.redis_client.ping()

    async def close_redis(self):
        if self.redis_client:
            await self.redis_client.close()

    async def set(self, key: str, value: str, expires: int = settings.DATA_CACHE_TTL):
        return await self.redis_client.setex(key, expires, value)

    async def get(self, key: str):
        return await self.redis_client.get(key)

    async def delete(self, key: str):
        return await self.redis_client.delete(key)

redis_cache = RedisCache()
