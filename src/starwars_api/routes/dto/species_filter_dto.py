from pydantic import BaseModel
from typing import Optional

class SpeciesFilterDto(BaseModel):
    name: Optional[str]
    classification: Optional[str]
    designation: Optional[str]
    average_height: Optional[str]
    average_lifespan: Optional[str]
    eye_colors: Optional[str]
    hair_colors: Optional[str]
    skin_colors: Optional[str]
    language: Optional[str]
    homeworld: Optional[str]
    url: Optional[str]
    created: Optional[str]
    edited: Optional[str]
    
    # arrays
    people: Optional[str]
    films: Optional[str]