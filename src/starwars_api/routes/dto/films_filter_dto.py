from pydantic import BaseModel
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
    species: Optional[List[str]] = None
    starships: Optional[List[str]] = None
    vehicles: Optional[List[str]] = None
    characters: Optional[List[str]] = None
    planets: Optional[List[str]] = None




