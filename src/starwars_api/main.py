from contextlib import asynccontextmanager
from logging import root
import os

from fastapi import FastAPI

from starwars_api.cache.cache import RedisCache
from starwars_api.routes.auth_router import router as auth_router
from starwars_api.routes.auth_router import warm_cache
from starwars_api.routes.swapi_router import router as swapi_router
from fastapi.responses import JSONResponse
from mangum import Mangum
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))



@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = RedisCache()
    try:
        await redis.connect()
        print("Connected to Redis successfully")
    except Exception as e:
        print(f"Warning: Could not connect to Redis: {e}")
    yield
    await redis.disconnect()


app = FastAPI(
    title="Star Wars API",
    description="A FastAPI implementation of the Star Wars API (SWAPI) with caching and sorting capabilities.",
    version="1.0.0",
    lifespan=lifespan,
    root_path="/deploy/swapi-function",
)

@app.get("/redis-test")
async def redis_test():
    redis = RedisCache()
    return {
        "status": "connected" if await redis.ping() else "disconnected",
        "redis_url": os.getenv("REDIS_URL")
    }
    
@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "ready"}, status_code=200)

app.include_router(auth_router)
app.include_router(swapi_router)

handler = Mangum(app, api_gateway_base_path="/deploy/swapi-function")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
