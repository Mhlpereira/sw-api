import asyncio
from typing import Dict, List
import httpx
from starwars_api.cache.cache import RedisCache
from tenacity import retry, stop_after_attempt, wait_exponential

class CacheWarmupService:
    def __init__(
        self,
        redis_cache: RedisCache,
        api_base_url: str = "https://swapi.info/api/",
        endpoints: List[str] = None,
        max_concurrent: int = 5,
        http_timeout: float = 30.0
    ):
        self.redis = redis_cache
        self.api_base_url = api_base_url
        self.endpoints = endpoints or ["people", "films", "starships", "vehicles", "species", "planets"]
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.timeout = http_timeout
        self.retry_policy = {
            "stop": stop_after_attempt(3),
            "wait": wait_exponential(multiplier=1, min=1, max=5)
        }

    async def _cache_data(self, key: str, data: any) -> bool:
        async with self.semaphore:
            return await self.redis.set(key, data, expire=3600)

    async def _fetch_data(self, endpoint: str, client: httpx.AsyncClient) -> Dict:
        try:
            response = await client.get(f"{self.api_base_url}/{endpoint}", timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error for {endpoint}: {e.response.status_code}")
            raise
        except Exception as e:
            print(f"Error fetching {endpoint}: {str(e)}")
            raise

    async def warm_endpoint(self, endpoint: str) -> int:
        async with httpx.AsyncClient() as client:
            data = await self._fetch_data(endpoint, client)
            if not data:
                return 0

            # Cache main endpoint data
            await self._cache_data(endpoint, data)
            
            # Cache individual items
            items = data.get("results", []) if isinstance(data, dict) else data
            if not isinstance(items, list):
                items = [items]

            tasks = [
                self._cache_data(item["url"], item)
                for item in items
                if item and isinstance(item, dict) and item.get("url")
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return sum(1 for r in results if r is True)

    async def warm_all(self) -> Dict[str, any]:
        if not await self.redis.ping():
            return {"status": "error", "message": "Redis connection failed"}

        tasks = [self.warm_endpoint(endpoint) for endpoint in self.endpoints]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        successful = [r for r in results if not isinstance(r, Exception)]
        failed = [i for i, r in enumerate(results) if isinstance(r, Exception)]
        
        return {
            "status": "partial" if failed else "success",
            "cached_items": sum(successful),
            "failed_endpoints": [self.endpoints[i] for i in failed] if failed else None
        }