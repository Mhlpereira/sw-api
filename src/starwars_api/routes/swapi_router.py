from fastapi import APIRouter, Depends
from service.swapi_service import SwapiService
from starwars_api.src.starwars_api.routes.dto.person_dto import PersonFilters


router = APIRouter()
swapi_service = SwapiService()

@router.get("/people")
async def list_people(filters: PersonFilters = Depends()):
    return await swapi_service.list_people(filters)

@router.get("/people/{person_id}")
async def get_people(id):
    return await swapi_service.get_people(id)

@router.get("/films")
async def list_films():
    return await swapi_service.list_films()

@router.get("/films/{film_id}")
async def get_films():
    return await swapi_service.get_films()

@router.get("/starships")
async def list_starships():
    return await swapi_service.list_starships()

@router.get("/starships/{starship_id}")
async def get_starships():
    return await swapi_service.get_starships()

@router.get("/vehicles")
async def list_vehicles():
    return await swapi_service.list_vehicles()

@router.get("/vehicles/{vehicle_id}")
async def get_vehicles():
    return await swapi_service.get_vehicles()

@router.get("/species")
async def list_species():
    return await swapi_service.list_species()

@router.get("/species/{species_id}")
async def get_species():    
    return await swapi_service.get_species()

@router.get("/planets")
async def list_planets():
    return await swapi_service.list_planets()

@router.get("/planets/{planet_id}")
async def get_planets():
    return await swapi_service.get_planets()