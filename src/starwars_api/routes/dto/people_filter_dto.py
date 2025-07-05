from pydantic import BaseModel
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
    film: Optional[List[str]] = None
    species: Optional[List[str]] = None
    starship: Optional[List[str]] = None
    vehicle: Optional[List[str]] = None
            


