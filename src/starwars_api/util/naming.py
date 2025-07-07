import json
from typing import Any, Dict, List, Optional

import httpx
from fastapi_cache import FastAPICache


async def url_to_name(urls: List[str]) -> List[Optional[str]]:
    try:
        cache = FastAPICache.get_backend()
        names = []

        for url in urls:
            cache_key = f"name:{url}"

            cached_name = await cache.get(cache_key)
            if cached_name:
                if isinstance(cached_name, (bytes, bytearray)):
                    cached_name = cached_name.decode("utf-8")
                names.append(cached_name)
                continue

            cached_data = await cache.get(url)
            if cached_data:
                try:
                    if isinstance(cached_data, (bytes, bytearray)):
                        cached_str = cached_data.decode("utf-8")
                    else:
                        cached_str = str(cached_data)

                    data: Dict[str, Any] = json.loads(cached_str)
                    name = data.get("name") or data.get("title")
                    names.append(name)

                    if name:
                        await cache.set(cache_key, name, expire=3600)
                    continue
                except (json.JSONDecodeError, AttributeError, UnicodeDecodeError):
                    pass

            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(url)
                    if response.status_code == 200:
                        data = response.json()
                        name = data.get("name") or data.get("title")
                        names.append(name)

                        await cache.set(
                            url, json.dumps(data).encode("utf-8"), expire=3600
                        )
                        if name:
                            await cache.set(
                                cache_key, name.encode("utf-8"), expire=3600
                            )
                    else:
                        names.append(None)
                except Exception:
                    names.append(None)

    except Exception:
        names = []
        for url in urls:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url)
                    if response.status_code == 200:
                        data = response.json()
                        name = data.get("name") or data.get("title")
                        names.append(name)
                    else:
                        names.append(None)
            except Exception:
                names.append(None)

    return names
