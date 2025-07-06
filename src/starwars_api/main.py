from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from starwars_api.cache import RedisCache
from dotenv import load_dotenv
from starwars_api.routes import auth_router, swapi_router



load_dotenv()

redis_cache = RedisCache(os.getenv("REDIS_URL"))

@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_cache.connect()
    yield
    await redis_cache.disconnect()


app = FastAPI(
    title="Star Wars API",
    description="A FastAPI implementation of the Star Wars API (SWAPI) with caching and sorting capabilities.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(swapi_router, prefix="/api/v1", tags=["swapi"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

