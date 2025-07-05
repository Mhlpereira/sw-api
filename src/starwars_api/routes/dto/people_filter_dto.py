from pydantic import BaseModel
from typing import Optional

class PersonFiltersDto(BaseModel):
    name: Optional[str]
    birth_year: Optional[str]
    eye_color: Optional[str]
    gender: Optional[str]
    hair_color: Optional[str]
    height: Optional[str]
    mass: Optional[str]
    skin_color: Optional[str]
    homeworld: Optional[str]
    
    #arrays
    film: Optional[str]
    species: Optional[str]
    starship: Optional[str]
    vehicle: Optional[str]
            


