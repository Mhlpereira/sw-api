from pydantic import BaseModel, HttpUrl
from typing import List, Optional



class StarshipsFilterDto(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    starship_class: Optional[str] = None
    manufacturer: Optional[str] = None
    cost_in_credits: Optional[str] = None
    length: Optional[str] = None
    crew: Optional[str] = None
    passengers: Optional[str] = None
    max_atmosphering_speed: Optional[str] = None
    hyperdrive_rating: Optional[str] = None
    MGLT: Optional[str] = None
    cargo_capacity: Optional[str] = None
    consumables: Optional[str] = None
    url: Optional[str] = None
    created: Optional[str] = None
    edited: Optional[str] = None
    
    #arrays
    films: Optional[List[HttpUrl]] = None
    pilots: Optional[List[HttpUrl]] = None
    
