
from starwars_api.util.naming import url_to_name


async def resolve_name_fields(data: dict, fields: list[str]) -> dict:
    for field in fields:
        if field in data:
            if isinstance(data[field], list):
                data[field] = await url_to_name(data[field])
            elif isinstance(data[field], str) and data[field].startswith("http"):
                resolved = await url_to_name([data[field]])
                data[field] = resolved[0] if resolved else None
    return data