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


@router.post("/auth", status_code=201, summary="Generate JWT Token")
async def authenticate():
    return await auth_service.generate_token()


@router.post("/warm-cache", status_code=200, summary="Warm up cache")
async def warm_cache():
    redis = RedisCache()
    try:
        if not await redis.connect():
            raise HTTPException(
                status_code=503,
                detail="Failed to connect to Redis"
            )

        warmup = CacheWarmupService(
            redis_cache=redis,
            request_delay=1.0,  
            timeout=30.0
        )
        
        result = await warmup.warm_all()
        
        return {
            "status": "success",
            "details": result,
            "message": f"Cache warmed up successfully. {result['total_cached']} items cached."
        }
        
    except HTTPException:
        raise  
    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to warm up cache",
            "error": str(e)
        }
    finally:
        try:
            await redis.disconnect()
        except Exception as e:
            print(f"Error closing Redis connection: {e}")

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
            await redis.disconnect()