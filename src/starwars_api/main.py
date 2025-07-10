from contextlib import asynccontextmanager

from fastapi import FastAPI

from starwars_api.cache import redis_cache
from starwars_api.routes.auth_router import router as auth_router
from starwars_api.routes.auth_router import warm_cache
from starwars_api.routes.swapi_router import router as swapi_router
from fastapi.responses import JSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await redis_cache.connect()
        await warm_cache()
    except Exception as e:
        print(f"Warning: Could not connect to Redis or warm cache: {e}")
    yield
    await redis_cache.disconnect()


app = FastAPI(
    title="Star Wars API",
    description="A FastAPI implementation of the Star Wars API (SWAPI) with caching and sorting capabilities.",
    version="1.0.0",
    lifespan=lifespan,
)

@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "ready"}, status_code=200)

app.include_router(auth_router)
app.include_router(swapi_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
