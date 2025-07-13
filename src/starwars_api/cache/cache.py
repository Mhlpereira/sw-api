import os
import json
from typing import Any, Optional, Union
from contextlib import asynccontextmanager
import redis.asyncio as redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from tenacity import retry, stop_after_attempt, wait_exponential

class RedisCache:
    _instance = None
    _redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    def __new__(cls, redis_url: str = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._redis_url = redis_url or os.getenv("REDIS_URL")
            if not cls._redis_url:
                raise ValueError("Redis URL must be provided via parameter or REDIS_URL environment variable")
        return cls._instance

    def __init__(self, redis_url: str = None):
        if not hasattr(self, '_initialized'):
            self.redis_url = redis_url or os.getenv("REDIS_URL")
            self.redis: Optional[redis.Redis] = None
            self._is_connected = False
            self._initialized = True

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def connect(self) -> None:
        if self._is_connected:
            return
            
        try:
            self.redis = await redis.from_url(
                self.redis_url,
                socket_timeout=2,
                socket_connect_timeout=2,
                max_connections=20,
                health_check_interval=30,
                retry_on_timeout=True
            )
            await self.redis.ping()
            self._is_connected = True
            FastAPICache.init(RedisBackend(self.redis), prefix="starwars_cache")
        except Exception as e:
            self._is_connected = False
            raise ConnectionError(f"Redis connection failed: {str(e)}")

    @asynccontextmanager
    async def get_connection(self):
        if not self._is_connected:
            await self.connect()
            
        try:
            yield self.redis
        except redis.RedisError as e:
            self._is_connected = False
            raise

    async def set(self, key: str, value: Union[str, dict, list], expire: int = 3600) -> bool:
        async with self.get_connection() as conn:
            try:
                serialized = json.dumps(value) if isinstance(value, (dict, list)) else value
                return await conn.set(key, serialized, ex=expire)
            except (redis.RedisError, json.JSONDecodeError):
                return False

    async def get(self, key: str) -> Optional[Any]:
        async with self.get_connection() as conn:
            try:
                value = await conn.get(key)
                if not value:
                    return None
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value.decode() if isinstance(value, bytes) else value
            except redis.RedisError:
                return None

    async def ping(self) -> bool:
        try:
            async with self.get_connection() as conn:
                return await conn.ping()
        except Exception:
            return False

    async def close(self):
        if self.redis and self._is_connected:
            await self.redis.close()
            self._is_connected = False