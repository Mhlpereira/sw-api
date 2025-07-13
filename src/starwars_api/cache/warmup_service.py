import asyncio
from typing import Any, Dict, Optional

import httpx
from starwars_api.cache.cache import RedisCache
from tenacity import retry, stop_after_attempt, wait_exponential

redis_cache = RedisCache()  

class CacheWarmupService:
    _MAX_CONCURRENT_REQUESTS = 5
    _CACHE_TTL = 3600 
    _HTTP_TIMEOUT = 30.0
    _RETRY_POLICY = {
        "stop": stop_after_attempt(3),
        "wait": wait_exponential(multiplier=1, min=1, max=5)
    }

    def __init__(self, api_base_url: str = "https://swapi.info/api/"):
        self.api_base_url = api_base_url
        self.semaphore = asyncio.Semaphore(self._MAX_CONCURRENT_REQUESTS)
        self.endpoints = ["people", "films", "starships", "vehicles", "species", "planets"]

    @retry(**_RETRY_POLICY)
    async def _cache_item(self, key: str, value: Any) -> bool:
        async with self.semaphore:
            return await redis_cache.set(key, value, expire=self._CACHE_TTL)

    async def _process_items(self, items: list[dict]) -> int:
        tasks = [
            self._cache_item(item["url"], item)
            for item in items
            if item.get("url")
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return sum(1 for result in results if result is True)

    async def _verify_redis_connection(self) -> bool:
        try:
            return await redis_cache.ping()
        except Exception:
            return False

    @retry(**_RETRY_POLICY)
    async def _fetch_endpoint_data(self, endpoint: str, client: httpx.AsyncClient) -> Optional[dict]:
        response = await client.get(f"{self.api_base_url}{endpoint}")
        response.raise_for_status()
        return response.json()

    async def _process_endpoint(self, endpoint: str, client: httpx.AsyncClient) -> int:
        try:
            data = await self._fetch_endpoint_data(endpoint, client)
            if not data:
                return 0

            await self._cache_item(endpoint, data)
            items = data["results"] if isinstance(data, dict) and "results" in data else data
            return await self._process_items(items if isinstance(items, list) else [items])

        except httpx.HTTPStatusError as e:
            print(f"HTTP error for {endpoint}: {e.response.status_code}")
        except Exception as e:
            print(f"Error processing {endpoint}: {str(e)}")
        return 0

    async def warm_up_cache(self) -> Dict[str, Any]:
        if not await self._verify_redis_connection():
            return {"status": "error", "message": "Redis connection failed"}

        async with httpx.AsyncClient(timeout=self._HTTP_TIMEOUT) as client:
            tasks = [self._process_endpoint(endpoint, client) for endpoint in self.endpoints]
            results = await asyncio.gather(*tasks)

        total_cached = sum(results)
        return {
            "status": "success",
            "cached_items": total_cached,
            "details": dict(zip(self.endpoints, results))
        }