from .cache import RedisCache

try:
    from .cache_instance import redis_cache

    __all__ = ["RedisCache", "redis_cache"]
except ImportError:
    __all__ = ["RedisCache"]
