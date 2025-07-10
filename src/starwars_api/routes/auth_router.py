from fastapi import APIRouter

from starwars_api.cache.warmup_service import cache_warmup_service
from starwars_api.services.auth_service import AuthService

router = APIRouter(
    prefix="/",
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
    return await cache_warmup_service.warm_up_cache()

@router.get("/health")
def health_check():
    return {"status": "ok"}