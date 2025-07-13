import asyncio
from typing import Dict, List
import httpx
from starwars_api.cache.cache import RedisCache
from tenacity import stop_after_attempt, wait_exponential

class CacheWarmupService:
    def __init__(
        self,
        api_base_url: str = "https://swapi.info/api/",
        endpoints: List[str] = None,
        max_concurrent: int = 5,
        http_timeout: float = 30.0,
        delay_between_items: float = 0.5  # ⏱️ Delay entre cada item
    ):
        self.api_base_url = api_base_url
        self.endpoints = endpoints or ["people", "films", "starships", "vehicles", "species", "planets"]
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.timeout = http_timeout
        self.delay = delay_between_items
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
        except Exception as e:
            print(f"Erro ao buscar {endpoint}: {e}")
            raise

    async def warm_endpoint(self, endpoint: str) -> int:
        async with httpx.AsyncClient() as client:
            data = await self._fetch_data(endpoint, client)
            if not data:
                return 0

            # Cache principal
            await self._cache_data(endpoint, data)
            
            # Cache itens individuais com delay entre cada um
            items = data.get("results", []) if isinstance(data, dict) else data
            if not isinstance(items, list):
                items = [items]

            cached_count = 0
            for item in items:
                if item and isinstance(item, dict) and item.get("url"):
                    try:
                        result = await self._cache_data(item["url"], item)
                        if result:
                            cached_count += 1
                    except Exception as e:
                        print(f"Erro ao cachear {item.get('url')}: {e}")
                    await asyncio.sleep(self.delay)  # 💤 Delay aqui
            return cached_count

    async def warm_all(self) -> Dict[str, any]:
        if not await self.redis.ping():
            return {"status": "error", "message": "Redis connection failed"}

        results = await asyncio.gather(*[self.warm_endpoint(endpoint) for endpoint in self.endpoints], return_exceptions=True)
        
        successful = [r for r in results if not isinstance(r, Exception)]
        failed = [self.endpoints[i] for i, r in enumerate(results) if isinstance(r, Exception)]

        return {
            "status": "partial" if failed else "success",
            "cached_items": sum(successful),
            "failed_endpoints": failed or None
        }
