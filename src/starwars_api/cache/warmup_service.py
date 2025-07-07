from typing import Any, Dict

import httpx

from starwars_api.cache import redis_cache


class CacheWarmupService:
    def __init__(self):
        self.api_url = "https://swapi.info/api/"

    async def warm_up_cache(self) -> Dict[str, Any]:
        try:
            cached_endpoints = {}
            total_cached_items = 0
            total_cached_names = 0

            endpoints = [
                "people",
                "films",
                "starships",
                "vehicles",
                "species",
                "planets",
            ]

            async with httpx.AsyncClient() as client:
                for endpoint in endpoints:
                    try:
                        response = await client.get(f"{self.api_url}{endpoint}")
                        if response.status_code == 200:
                            data = response.json()

                            await redis_cache.set(endpoint, data, expire=3600)

                            count = 0
                            if "results" in data and isinstance(data["results"], list):
                                count = len(data["results"])
                                total_cached_items += count
                                total_cached_names += count

                            cached_endpoints[endpoint] = count
                    except Exception:
                        cached_endpoints[endpoint] = 0

            return {
                "message": "Cache warmed successfully",
                "cached_endpoints": cached_endpoints,
                "total_cached_items": total_cached_items,
                "total_cached_names": total_cached_names,
            }

        except Exception as e:
            return {"message": "Cache warming failed", "error": str(e)}


cache_warmup_service = CacheWarmupService()
