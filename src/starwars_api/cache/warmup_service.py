import asyncio
from typing import Any, Dict

import httpx

from starwars_api.cache import redis_cache


class CacheWarmupService:
    def __init__(self):
        self.api_url = "https://swapi.info/api/"
        self.max_retries = 3
        self.retry_delay = 1
        self.semaphore = asyncio.Semaphore(5)

    async def _safe_cache_operation(self, operation, *args, **kwargs):
        async with self.semaphore:
            for attempt in range(self.max_retries):
                try:
                    return await operation(*args, **kwargs)
                except Exception as e:
                    if attempt < self.max_retries - 1:
                        print(f"⚠️ Tentativa {attempt + 1} falhou, tentando novamente em {self.retry_delay}s...")
                        await asyncio.sleep(self.retry_delay)
                    else:
                        print(f"❌ Operação falhou após {self.max_retries} tentativas: {str(e)}")
                        return None

    async def _cache_item_with_retry(self, key: str, value: Any) -> bool:
        result = await self._safe_cache_operation(redis_cache.set, key, value, expire=3600)
        return result is not None

    async def _process_endpoint_items(self, data: Dict[str, Any]) -> int:
        count = 0
        if isinstance(data, list):
            tasks = []
            for item in data:
                item_url = item.get("url")
                if item_url:
                    task = self._cache_item_with_retry(item_url, item)
                    tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            count = sum(1 for r in results if r is True)

        elif isinstance(data, dict) and "results" in data:
            tasks = []
            for item in data["results"]:
                item_url = item.get("url")
                if item_url:
                    task = self._cache_item_with_retry(item_url, item)
                    tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            count = sum(1 for r in results if r is True)

        return count

    async def _test_redis_connection(self) -> bool:
        print("🔄 Testando conexão inicial com Redis...")
        test_result = await self._safe_cache_operation(redis_cache.exists, "test_connection_key")
        if test_result is not None:
            print("✅ Conexão com Redis: ESTABELECIDA COM SUCESSO!")
            return True
        else:
            print("❌ Falha na conexão inicial com Redis")
            return False

    async def _process_single_endpoint(self, endpoint: str, client: httpx.AsyncClient) -> int:
        try:
            print(f"🔄 Processando endpoint: {endpoint}")
            response = await client.get(f"{self.api_url}{endpoint}")

            if response.status_code == 200:
                data = response.json()

                print(f"💾 Cacheando endpoint principal: {endpoint}")
                await self._safe_cache_operation(redis_cache.set, endpoint, data, expire=3600)

                count = await self._process_endpoint_items(data)
                print(f"💾 Cached {count} items para {endpoint}")
                return count
            else:
                print(f"❌ Erro HTTP {response.status_code} para {endpoint}")
                return 0

        except Exception as e:
            print(f"❌ Erro processando endpoint {endpoint}: {str(e)}")
            return 0

    async def warm_up_cache(self) -> Dict[str, Any]:
        try:
            if not await self._test_redis_connection():
                return {"message": "Cache warming failed", "error": "Redis connection failed"}

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

            async with httpx.AsyncClient(timeout=30.0) as client:
                for endpoint in endpoints:
                    count = await self._process_single_endpoint(endpoint, client)
                    cached_endpoints[endpoint] = count
                    total_cached_items += count
                    total_cached_names += count

            print(f"✅ Cache warming concluído! Total de itens: {total_cached_items}")
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
