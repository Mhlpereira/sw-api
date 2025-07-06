import httpx


async def url_to_name(urls: list[str]) -> list[str]:
    # cache = FastAPICache.get_backend()  # Temporariamente desabilitado
    names = []

    for url in urls:
        # cached = await cache.get(url)  # Temporariamente desabilitado
        # if cached:
        #     names.append(cached.get("name") or cached.get("title"))
        # else:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                name = data.get("name") or data.get("title")
                names.append(name)
                # await cache.set(url, data, expire=3600)  # Temporariamente desabilitado
            else:
                names.append(None)

    return names
