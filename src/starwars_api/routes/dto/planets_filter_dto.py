from pydantic import BaseModel
from typing import Optional

class SpeciesFilterDto(BaseModel):
    name: Optional[str]
    diameter: Optional[str]
    rotation_period: Optional[str]
    orbital_period: Optional[str]
    gravity: Optional[str]
    population: Optional[str]
    climate: Optional[str]
    terrain: Optional[str]
    surface_water: Optional[str]
    url: Optional[str]
    created: Optional[str]
    edited: Optional[str]
    
    #arrays
    residents: Optional[str]
    films: Optional[str]