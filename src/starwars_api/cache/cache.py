import json
from typing import Any, Optional, Union
from functools import wraps
from contextlib import asynccontextmanager
import redis.asyncio as redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from tenacity import retry, stop_after_attempt, wait_exponential

class RedisCache:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, redis_url: str):
        if not hasattr(self, 'redis'):
            self.redis_url = redis_url
            self.redis: Optional[redis.Redis] = None
            self._is_connected = False

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
            print("✅ Conexão Redis estabelecida com sucesso")
        except Exception as e:
            print(f"❌ Falha na conexão Redis: {str(e)}")
            self._is_connected = False
            raise

    @asynccontextmanager
    async def connection(self):
        if not self._is_connected:
            await self.connect()
            
        try:
            yield self.redis
        except redis.RedisError as e:
            print(f"⚠️ Erro Redis: {str(e)}")
            self._is_connected = False
            raise

    async def set(self, 
                 key: str, 
                 value: Union[str, dict, list], 
                 expire: int = 3600) -> bool:

        async with self.connection() as conn:
            try:
                serialized = json.dumps(value) if isinstance(value, (dict, list)) else value
                await conn.set(key, serialized, ex=expire)
                return True
            except (redis.RedisError, json.JSONDecodeError) as e:
                print(f"⚠️ Falha ao armazenar cache: {str(e)}")
                return False

    async def get(self, key: str) -> Optional[Any]:
        async with self.connection() as conn:
            try:
                value = await conn.get(key)
                if not value:
                    return None
                    
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value.decode('utf-8') if isinstance(value, bytes) else value
            except redis.RedisError as e:
                print(f"⚠️ Falha ao obter cache: {str(e)}")
                return None

    async def exists(self, key: str) -> bool:
        async with self.connection() as conn:
            try:
                return await conn.exists(key) == 1
            except redis.RedisError:
                return False

    async def disconnect(self) -> None:
        if self.redis and self._is_connected:
            await self.redis.close()
            self._is_connected = False

def cache_response(ttl: int = 600):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache = RedisCache.instance()
            cache_key = f"{func.__name__}:{str(kwargs)}"
            
            if await cache.exists(cache_key):
                return await cache.get(cache_key)
                
            result = await func(*args, **kwargs)
            await cache.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator