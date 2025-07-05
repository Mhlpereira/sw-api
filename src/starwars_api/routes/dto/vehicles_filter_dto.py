from pydantic import BaseModel
from typing import Optional


class VehicleFilterDto(BaseModel):
    name: Optional[str]
    model: Optional[str]
    vehicle_class: Optional[str]
    manufacturer: Optional[str]
    length: Optional[str]
    cost_in_credits: Optional[str]
    crew: Optional[str]
    passengers: Optional[str]
    max_atmosphering_speed: Optional[str]
    cargo_capacity: Optional[str]
    consumables: Optional[str]
    url: Optional[str]
    created: Optional[str]
    edited: Optional[str]
    
    #arrays
    films: Optional[str]
    pilots: Optional[str]