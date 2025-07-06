from pydantic import BaseModel
from typing import Optional


class FilmsFilterDto(BaseModel):
    title: Optional[str] = None
    episode_id: Optional[int] = None
    opening_crawl: Optional[str] = None
    director: Optional[str] = None
    producer: Optional[str] = None
    release_date: Optional[str] = None
    url: Optional[str] = None
    created: Optional[str] = None
    edited: Optional[str] = None
    
    # Para arrays, usar strings separadas por vírgula como query params
    species: Optional[str] = None
    starships: Optional[str] = None
    vehicles: Optional[str] = None
    characters: Optional[str] = None
    planets: Optional[str] = None


