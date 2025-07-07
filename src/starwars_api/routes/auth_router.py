from fastapi import APIRouter

from starwars_api.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

auth_service = AuthService()


# Endpoint to generate JWT token
@router.post("/auth", status_code=201, summary="Generate JWT Token")
async def authenticate():
    return await auth_service.generate_token()


# Endpoint to warm up / seed the cache
