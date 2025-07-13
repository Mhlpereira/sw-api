from contextlib import asynccontextmanager
import os
import json
import redis.asyncio as redis
from typing import Any, Optional, Union

class RedisCache:
    def __init__(self):
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.connection = None

    async def connect(self):
        if not self.connection:
            try:
                self.connection = await redis.from_url(
                    self.redis_url,
                    socket_timeout=2,
                    socket_connect_timeout=2
                )
                await self.connection.ping()
                return True
            except Exception as e:
                self.connection = None
                raise ConnectionError(f"Redis connection failed: {str(e)}")
        return True

    async def disconnect(self):
        if self.connection:
            await self.connection.close()
            self.connection = None

    async def set(self, key: str, value: Union[str, dict, list], expire: int = 3600) -> bool:
        try:
            serialized = json.dumps(value) if isinstance(value, (dict, list)) else value
            return await self.connection.set(key, serialized, ex=expire)
        except Exception:
            return False

    async def get(self, key: str) -> Optional[Any]:
        try:
            value = await self.connection.get(key)
            if value:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value.decode() if isinstance(value, bytes) else value
            return None
        except Exception:
            return None

    async def ping(self) -> bool:
        try:
            return await self.connection.ping()
        except Exception:
            return False
        
    @asynccontextmanager
    async def get_connection(self):
        await self._ensure_connection()
        try:
            yield self.connection
        finally:
            # Não fechamos a conexão aqui, mantemos pooling
            pass