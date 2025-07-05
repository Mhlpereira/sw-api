from fastapi import FastAPI
from routes.swapi_router import router as swapi_router

app = FastAPI(
    title="Star Wars API",
    description="API para dados do Star Wars",
    version="1.0.0"
)


app.include_router(swapi_router, prefix="/api/v1", tags=["swapi"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

