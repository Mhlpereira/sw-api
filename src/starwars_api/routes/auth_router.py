from fastapi import APIRouter
from starwars_api.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


auth_service = AuthService()

@router.post("/auth", status_code=201)
async def authenticate():
    return await auth_service.authenticate()