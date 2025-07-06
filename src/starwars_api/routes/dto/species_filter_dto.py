from pydantic import BaseModel
from typing import Optional




class SpeciesFilterDto(BaseModel):
    name: Optional[str] = None
    classification: Optional[str] = None
    designation: Optional[str] = None
    average_height: Optional[str] = None
    average_lifespan: Optional[str] = None
    eye_colors: Optional[str] = None
    hair_colors: Optional[str] = None
    skin_colors: Optional[str] = None
    language: Optional[str] = None
    homeworld: Optional[str] = None
    url: Optional[str] = None
    created: Optional[str] = None
    edited: Optional[str] = None
    
    # arrays
    people: Optional[str] = None
    films: Optional[str] = None
    
