import os
from fastapi import APIRouter
from starwars_api.cache.cache import RedisCache
from starwars_api.cache.warmup_service import CacheWarmupService
from starwars_api.services.auth_service import AuthService

router = APIRouter(
    prefix="",
    tags=["Authentication"],
)

auth_service = AuthService()
cache_warmup_service = CacheWarmupService()
redis= RedisCache()


# Endpoint to generate JWT token
@router.post("/auth", status_code=201, summary="Generate JWT Token")
async def authenticate():
    return await auth_service.generate_token()


# Endpoint to warm up / seed the cache
@router.post("/warm-cache", status_code=200, summary="Warm up cache")
async def warm_cache():
        CacheWarmupService(redis_cache=redis, delay_between_items=1.0)


@router.get("/debug-env")
async def debug_env():
    return {
        "JWT_SECRET_KEY": os.getenv("JWT_SECRET_KEY", "NOT_FOUND")[:20] + "...",  # Só os primeiros 20 chars
        "REDIS_URL": os.getenv("REDIS_URL", "NOT_FOUND")[:20] + "...",
        "env_loaded": "JWT_SECRET_KEY" in os.environ
    }