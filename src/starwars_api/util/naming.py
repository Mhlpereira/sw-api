import json
from typing import List, Optional

import httpx

from starwars_api.cache import redis_cache


async def url_to_name(urls: List[str]) -> List[Optional[str]]:
    try:
        names = []
        cache_hits = 0
        cache_misses = 0

        async with httpx.AsyncClient() as client:
            for url in urls:
                try:
                    cache_key = f"name:{url}"
                    cached_name = await redis_cache.get(cache_key)

                    if cached_name:
                        if isinstance(cached_name, (bytes, bytearray)):
                            cached_name = cached_name.decode("utf-8")
                        names.append(cached_name)
                        cache_hits += 1
                        continue

                    cached_data = await redis_cache.get(url)
                    if cached_data:
                        try:
                            if isinstance(cached_data, (bytes, bytearray)):
                                cached_str = cached_data.decode("utf-8")
                            else:
                                cached_str = str(cached_data)

                            data = json.loads(cached_str)
                            name = data.get("name") or data.get("title")

                            if name:
                                await redis_cache.set(cache_key, name, expire=3600)
                                names.append(name)
                                cache_hits += 1
                                continue
                        except (
                            json.JSONDecodeError,
                            AttributeError,
                            UnicodeDecodeError,
                        ) as e:
                            print(f"Erro ao processar cache para {url}: {str(e)}")

                    cache_misses += 1
                    response = await client.get(url, timeout=10.0)

                    if response.status_code == 200:
                        data = response.json()
                        name = data.get("name") or data.get("title")
                        names.append(name)

                        await redis_cache.set(url, json.dumps(data), expire=3600)
                        if name:
                            await redis_cache.set(cache_key, name, expire=3600)
                    else:
                        names.append(None)

                except httpx.TimeoutException:
                    print(f"Timeout ao acessar {url}")
                    names.append(None)
                except httpx.RequestError as e:
                    print(f"Erro na requisição para {url}: {str(e)}")
                    names.append(None)
                except Exception as e:
                    print(f"Erro inesperado processando {url}: {str(e)}")
                    names.append(None)

        print(
            f"Cache stats - Total URLs: {len(urls)}, Hits: {cache_hits}, Misses: {cache_misses}"
        )

        return names
    except Exception as e:
        print(f"Erro geral na função url_to_name: {str(e)}")
        return [None] * len(urls)
