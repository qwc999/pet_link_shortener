import redis.asyncio as redis

from app.config import settings


class RedisCache:
    async def init_redis(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses = True,
            encoding = "utf-8")
        await self.redis_client.ping()


redis_cache = RedisCache()