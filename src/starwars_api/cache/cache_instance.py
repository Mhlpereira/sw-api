import os

from dotenv import load_dotenv

from .cache import RedisCache

load_dotenv()

redis_cache = RedisCache(os.getenv("REDIS_URL", "redis://localhost:6379"))
