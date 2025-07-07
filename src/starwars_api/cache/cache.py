import json
from typing import Any, Union

import redis.asyncio as redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


class RedisCache:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis = None

    async def connect(self):
        try:
            self.redis = await redis.from_url(self.redis_url)
            FastAPICache.init(RedisBackend(self.redis), prefix="starwars_cache")
        except Exception as exception:
            print(f"Failed to connect to Redis: {exception}")
            self.redis = None

    async def set(self, key: str, value: Union[str, dict, list], expire: int = 3600):
        if not self.redis:
            return False
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            await self.redis.set(key, value, ex=expire)
            return True
        except Exception as exception:
            print(f"Failed to set cache for key {key}: {exception}")
            return False

    async def get(self, key: str) -> Any:
        if not self.redis:
            return None
        try:
            value = await self.redis.get(key)
            if value is None:
                return None

            if isinstance(value, (bytes, bytearray)):
                value = value.decode("utf-8")

            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        except Exception as exception:
            print(f"Failed to get cache for key {key}: {exception}")
            return None

    async def exists(self, key: str) -> bool:
        if not self.redis:
            return False
        try:
            return await self.redis.exists(key) > 0
        except Exception:
            return False

    async def disconnect(self):
        if self.redis:
            await self.redis.close()
