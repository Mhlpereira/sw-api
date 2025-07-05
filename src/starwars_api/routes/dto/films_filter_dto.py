from pydantic import BaseModel, HttpUrl
from typing import List, Optional


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
    
    #arrays
    species: Optional[List[HttpUrl]] = None
    starships: Optional[List[HttpUrl]] = None
    vehicles: Optional[List[HttpUrl]] = None
    characters: Optional[List[HttpUrl]] = None
    planets: Optional[List[HttpUrl]] = None


