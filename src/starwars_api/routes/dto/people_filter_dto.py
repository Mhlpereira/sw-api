from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class PersonFiltersDto(BaseModel):
    name: Optional[str] = None
    birth_year: Optional[str] = None
    eye_color: Optional[str] = None
    gender: Optional[str] = None
    hair_color: Optional[str] = None
    height: Optional[str] = None
    mass: Optional[str] = None
    skin_color: Optional[str] = None
    homeworld: Optional[str] = None
    
    #arrays
    film: Optional[List[HttpUrl]] = None
    species: Optional[List[HttpUrl]] = None
    starship: Optional[List[HttpUrl]] = None
    vehicle: Optional[List[HttpUrl]] = None

