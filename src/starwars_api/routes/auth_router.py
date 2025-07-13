from http.client import HTTPException
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


# Endpoint to generate JWT token
@router.post("/auth", status_code=201, summary="Generate JWT Token")
async def authenticate():
    return await auth_service.generate_token()


# Endpoint to warm up / seed the cache
@router.post("/warm-cache", status_code=200, summary="Warm up cache")
async def warm_cache():
    redis = None
    try:
        redis = RedisCache()

        if not await redis.ping():
            raise HTTPException(status_code=503, detail="Redis connection failed")
        
        warmupInstance = CacheWarmupService(redis_cache=redis, delay_between_items=1.0)
        result = await warmupInstance.warm_all()
        return {"message": "Cache warmed up successfully", "result": result}
    except Exception as e:
        return {"message": "Error warming up cache", "error": str(e)}
    finally:
        if redis.is_connected:
            try:
                await redis.disconnect()
            except Exception as e:
                print(f"Error disconnecting Redis: {e}")

@router.get("/redis-health")
async def redis_health():
    redis = None
    try:
        redis = RedisCache()
        ping_result = await redis.ping()
        return {
            "status": "connected" if ping_result else "disconnected",
            "redis_url": os.getenv("REDIS_URL", "NOT_FOUND")[:50] + "...",
            "ping_result": ping_result
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "redis_url": os.getenv("REDIS_URL", "NOT_FOUND")[:50] + "..."
        }
    finally:
        if redis:
            try:
                await redis.close()
            except:
                pass