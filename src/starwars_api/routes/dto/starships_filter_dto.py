from pydantic import BaseModel
from typing import Optional

class StarshipsFiltersDto(BaseModel):
    name: Optional[str]
    model: Optional[str]
    starship_class: Optional[str]
    manufacturer: Optional[str]
    cost_in_credits: Optional[str]
    length: Optional[str]
    crew: Optional[str]
    passengers: Optional[str]
    max_atmosphering_speed: Optional[str]
    hyperdrive_rating: Optional[str]
    MGLT: Optional[str]
    cargo_capacity: Optional[str]
    consumables: Optional[str]
    url: Optional[str]
    created: Optional[str]
    edited: Optional[str]
    
    #arrays
    films: Optional[str]
    pilots: Optional[str]
