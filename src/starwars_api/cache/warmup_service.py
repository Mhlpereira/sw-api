from typing import Any, Dict

import httpx

from starwars_api.cache import redis_cache


class CacheWarmupService:
    def __init__(self):
        self.api_url = "https://swapi.info/api/"

    async def warm_up_cache(self) -> Dict[str, Any]:
        try:
            await redis_cache.exists("test_connection_key")
            print("✅ Conexão com Redis: ESTABELECIDA COM SUCESSO!")

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
                            if isinstance(data, list):
                                for item in data:
                                    item_url = item.get("url")
                                    if item_url:
                                        await redis_cache.set(
                                            item_url, item, expire=3600
                                        )
                                        count += 1

                                total_cached_items += count
                                total_cached_names += count
                                print(f"💾 Cached {count} items para {endpoint}")

                            elif isinstance(data, dict) and "results" in data:
                                for item in data["results"]:
                                    item_url = item.get("url")
                                    if item_url:
                                        await redis_cache.set(
                                            item_url, item, expire=3600
                                        )
                                        count += 1

                                total_cached_items += count
                                total_cached_names += count

                            cached_endpoints[endpoint] = count
                        else:
                            cached_endpoints[endpoint] = 0

                    except Exception:
                        cached_endpoints[endpoint] = 0

            return {
                "message": "Cache warmed successfully",
                "cached_endpoints": cached_endpoints,
                "total_cached_items": total_cached_items,
                "total_cached_names": total_cached_names,
            }
        except Exception as e:
            print(f"❌ Erro geral no warm-up: {str(e)}")
            return {"message": "Cache warming failed", "error": str(e)}


cache_warmup_service = CacheWarmupService()
