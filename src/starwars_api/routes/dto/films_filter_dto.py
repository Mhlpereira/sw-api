from pydantic import BaseModel
from typing import Optional


class FilmsFilterDTO(BaseModel):
    title: Optional[str]
    episode_id: Optional[int]
    opening_crawl: Optional[str]
    director: Optional[str]
    producer: Optional[str]
    release_date: Optional[str]
    url: Optional[str]
    created: Optional[str]
    edited: Optional[str]
    
    #arrays
    species: Optional[str]
    starships: Optional[str]
    vehicles: Optional[str]
    characters: Optional[str]
    planets: Optional[str]




