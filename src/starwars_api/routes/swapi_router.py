from fastapi import APIRouter, Depends
from ..services.swapi_service import SwapiService
from .dto import (
    FilmsFilterDto,
    PeopleFilterDto,
    PlanetsFilterDto,
    SpeciesFilterDto,
    StarshipsFilterDto,
    VehiclesFilterDto
)


router = APIRouter()
swapi_service = SwapiService()

@router.get("/people")
async def list_people(filters: PeopleFilterDto = Depends()):
    return await swapi_service.list_people(filters)

@router.get("/people/{person_id}")
async def get_people(person_id: str):
    return await swapi_service.get_people(person_id)

@router.get("/films")
async def list_films(filters: FilmsFilterDto = Depends()):
    return await swapi_service.list_films(filters)

@router.get("/films/{film_id}")
async def get_films(film_id: str):
    return await swapi_service.get_films(film_id)

@router.get("/starships")
async def list_starships(filters: StarshipsFilterDto = Depends()):
    return await swapi_service.list_starships(filters)

@router.get("/starships/{starship_id}")
async def get_starships(starship_id: str):
    return await swapi_service.get_starships(starship_id)

@router.get("/vehicles")
async def list_vehicles(filters: VehiclesFilterDto = Depends()):
    return await swapi_service.list_vehicles(filters)

@router.get("/vehicles/{vehicle_id}")
async def get_vehicles(vehicle_id: str):
    return await swapi_service.get_vehicles(vehicle_id)

@router.get("/species")
async def list_species(filters: SpeciesFilterDto = Depends()):
    return await swapi_service.list_species(filters)

@router.get("/species/{species_id}")
async def get_species(species_id: str):    
    return await swapi_service.get_species(species_id)

@router.get("/planets")
async def list_planets(filters: PlanetsFilterDto = Depends()):
    return await swapi_service.list_planets(filters)

@router.get("/planets/{planet_id}")
async def get_planets(planet_id: str):
    return await swapi_service.get_planets(planet_id)