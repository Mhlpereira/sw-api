from pydantic import BaseModel
from typing import Optional


class PeopleFilterDto(BaseModel):
    name: Optional[str] = None
    birth_year: Optional[str] = None
    eye_color: Optional[str] = None
    gender: Optional[str] = None
    hair_color: Optional[str] = None
    height: Optional[str] = None
    mass: Optional[str] = None
    skin_color: Optional[str] = None
    homeworld: Optional[str] = None
    
    # Para arrays, usar strings separadas por vírgula como query params
    film: Optional[str] = None
    species: Optional[str] = None
    starship: Optional[str] = None
    vehicle: Optional[str] = None

