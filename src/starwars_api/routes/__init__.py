from starwars_api.routes.auth_router import router as auth_router
from starwars_api.routes.swapi_router import router as swapi_router

__all__ = ["auth_router", "swapi_router"]
