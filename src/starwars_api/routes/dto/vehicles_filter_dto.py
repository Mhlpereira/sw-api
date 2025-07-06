from pydantic import BaseModel
from typing import Optional


class VehiclesFilterDto(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    vehicle_class: Optional[str] = None
    manufacturer: Optional[str] = None
    length: Optional[str] = None
    cost_in_credits: Optional[str] = None
    crew: Optional[str] = None
    passengers: Optional[str] = None
    max_atmosphering_speed: Optional[str] = None
    cargo_capacity: Optional[str] = None
    consumables: Optional[str] = None
    url: Optional[str] = None
    created: Optional[str] = None
    edited: Optional[str] = None
    
    #arrays
    films: Optional[str] = None
    pilots: Optional[str] = None
    
