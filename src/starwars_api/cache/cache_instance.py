import os
from dotenv import load_dotenv
from .redis_cache import RedisCache

load_dotenv()

def get_redis_cache(redis_url: str = None) -> RedisCache:
    return RedisCache(redis_url or os.getenv("REDIS_URL"))