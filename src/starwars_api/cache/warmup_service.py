import asyncio
import httpx
from typing import Dict, List
from starwars_api.cache.cache import RedisCache

class CacheWarmupService:
    def __init__(
        self,
        redis_cache: RedisCache,
        api_base_url: str = "https://swapi.info/api/",
        endpoints: List[str] = None,
        request_delay: float = 0.5,
        timeout: float = 30.0
    ):
        self.redis = redis_cache
        self.api_base_url = api_base_url.rstrip('/')
        self.endpoints = endpoints or ["films", "people", "planets", "species", "vehicles", "starships"]
        self.delay = request_delay
        self.timeout = timeout
        
        self.resolvable_fields = {
            "films": ["characters", "planets", "starships", "vehicles", "species"],
            "people": ["homeworld", "films", "species", "starships", "vehicles"],
            "planets": ["residents", "films"],
            "species": ["homeworld", "people", "films"],
            "vehicles": ["pilots", "films"],
            "starships": ["pilots", "films"]
        }

    async def _fetch_all_pages(self, endpoint: str) -> List[Dict]:
        items = []
        url = f"{self.api_base_url}/{endpoint}"
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            while url:
                try:
                    response = await client.get(url)
                    response.raise_for_status()
                    data = response.json()
                    
                    items.extend(data.get('results', []))
                    url = data.get('next')
                    
                    if url:
                        await asyncio.sleep(self.delay)
                except Exception as e:
                    print(f"Error fetching {url}: {str(e)}")
                    break
        
        return items


    async def warm_endpoint(self, endpoint: str) -> Dict[str, any]:
        items = await self._fetch_all_pages(endpoint)
        success_count = 0
        
        for item in items:
            if await self._process_and_cache_item(endpoint, item):
                success_count += 1
            await asyncio.sleep(self.delay)  # Delay entre itens
        
        return {
            "endpoint": endpoint,
            "total_items": len(items),
            "cached_items": success_count
        }

    async def warm_all(self) -> Dict[str, any]:
        results = []
        
        for endpoint in self.endpoints:
            result = await self.warm_endpoint(endpoint)
            results.append(result)
            print(f"Warmed up {endpoint}: {result['cached_items']}/{result['total_items']} items")
            await asyncio.sleep(self.delay)  # Delay entre endpoints
        
        total_cached = sum(r['cached_items'] for r in results)
        total_items = sum(r['total_items'] for r in results)
        
        return {
            "status": "completed",
            "total_endpoints": len(self.endpoints),
            "total_items": total_items,
            "total_cached": total_cached,
            "details": results
        }