from pydantic import BaseModel
from typing import Optional



class PlanetsFilterDto(BaseModel):
    name: Optional[str] = None
    diameter: Optional[str] = None
    rotation_period: Optional[str] = None
    orbital_period: Optional[str] = None
    gravity: Optional[str] = None
    population: Optional[str] = None
    climate: Optional[str] = None
    terrain: Optional[str] = None
    surface_water: Optional[str] = None
    url: Optional[str] = None
    created: Optional[str] = None
    edited: Optional[str] = None
    
    #arrays
    residents: Optional[str] = None
    films:  Optional[str] = None
