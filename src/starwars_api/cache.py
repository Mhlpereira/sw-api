from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis



class RedisCache:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis = None

    async def connect(self):
        self.redis = await redis.from_url(self.redis_url)
        FastAPICache.init(RedisBackend(self.redis), prefix="starwars_cache")
        
    async def set(self, key: str, value: str, expire: int = 3600):
        if not self.redis:
            raise RuntimeError("Redis connection is not established.")
        await self.redis.set(key, value, ex=expire)

    async def get(self, key: str):
        if not self.redis:
            raise RuntimeError("Redis connection is not established.")
        return await self.redis.get(key)

    async def disconnect(self):
        if self.redis:
            await self.redis.close()