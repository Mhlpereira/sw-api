from typing import Optional
import httpx
from fastapi import HTTPException
from starwars_api.enums.order_enum import Order
from starwars_api.util import DataSorter, resolve_name_fields 
from starwars_api.routes.dto import (
    FilmsFilterDto,
    PeopleFilterDto,
    PlanetsFilterDto,
    SpeciesFilterDto,
    StarshipsFilterDto,
    VehiclesFilterDto
)



class SwapiService:

    def __init__(self):
        self.api_url = "https://swapi.info/api/"

async def list_people(self, filters: PeopleFilterDto=None, sort_by: Optional[str] =None, order: Order = Order.ASC):
        try:
            
            api_params = filters.model_dump(exclude_none=True) if filters else {}

            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}people", params=api_params)
                response.raise_for_status()
                data = response.json()
                
                if sort_by:
                    data["results"] = DataSorter.apply_sorting(data["results"], sort_by, order)
                
                
                formatted_results = await resolve_name_fields(data["results"], ["homeworld", "films", "species", "vehicles", "starships"])
                
                return formatted_results
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        
async def get_people(self, person_id: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}people/{person_id}")
                response.raise_for_status()
                data = response.json()
                
                formatted_results = await resolve_name_fields(data["results"], ["homeworld", "films", "species", "vehicles", "starships"])
                
                return formatted_results
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        
async def list_films(self, filters: FilmsFilterDto=None, sort_by: Optional[str] = None, order: Order = Order.ASC):
        try:
            api_params = filters.model_dump(exclude_none=True) if filters else {}
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}films", params=api_params)
                response.raise_for_status()
                data = response.json()
                
                if sort_by:
                    data["results"] = DataSorter.apply_sorting(data["results"], sort_by, order)
                
                formatted_results = await resolve_name_fields(data["results"], ["homeworld", "films", "species", "vehicles", "starships"])
                
                return formatted_results
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        
async def get_films(self, film_id: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}films/{film_id}")
                response.raise_for_status()
                data = response.json()
                
                formatted_results = await resolve_name_fields(data["results"], ["homeworld", "films", "species", "vehicles", "starships"])
                
                return formatted_results
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        
async def list_starships(self, filters: StarshipsFilterDto=None, sort_by: Optional[str] = None, order: Order = Order.ASC):
        try:
            api_params = filters.model_dump(exclude_none=True) if filters else {}
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}starships", params=api_params)
                response.raise_for_status()
                data = response.json()
                
                if sort_by:
                    data["results"] = DataSorter.apply_sorting(data["results"], sort_by, order)
                
                formatted_results = await resolve_name_fields(data["results"], ["homeworld", "films", "species", "vehicles", "starships"])
                
                return formatted_results
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        
async def get_starships(self, starship_id: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}starships/{starship_id}")
                response.raise_for_status()
                data = response.json()
                
                formatted_results = await resolve_name_fields(data["results"], ["homeworld", "films", "species", "vehicles", "starships"])
                
                return formatted_results
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

async def list_vehicles(self, filters: VehiclesFilterDto=None, sort_by: Optional[str] = None, order: Order = Order.ASC):
        try:
            api_params = filters.model_dump(exclude_none=True) if filters else {}
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}vehicles", params=api_params)
                response.raise_for_status()
                data = response.json()
                                
                if sort_by:
                    data["results"] = DataSorter.apply_sorting(data["results"], sort_by, order)
                
                formatted_results = await resolve_name_fields(data["results"], ["homeworld", "films", "species", "vehicles", "starships"])
                
                return formatted_results
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        
async def get_vehicles(self, vehicle_id: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}vehicles/{vehicle_id}")
                response.raise_for_status()
                data = response.json()
                
                formatted_results = await resolve_name_fields(data["results"], ["homeworld", "films", "species", "vehicles", "starships"])
                
                return formatted_results
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

async def list_species(self, filters: SpeciesFilterDto=None, sort_by: Optional[str] = None, order: Order = Order.ASC):
        try:
            api_params = filters.model_dump(exclude_none=True) if filters else {}
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}species", params=api_params)
                response.raise_for_status()
                data = response.json()
                                
                if sort_by:
                    data["results"] = DataSorter.apply_sorting(data["results"], sort_by, order)
                
                formatted_results = await resolve_name_fields(data["results"], ["homeworld", "films", "species", "vehicles", "starships"])
                
                return formatted_results
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

async def get_species(self, species_id: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}species/{species_id}")
                response.raise_for_status()
                data = response.json()
                
                formatted_results = await resolve_name_fields(data["results"], ["homeworld", "films", "species", "vehicles", "starships"])
                
                return formatted_results
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

async def list_planets(self, filters: PlanetsFilterDto=None, sort_by: Optional[str] = None, order: Order = Order.ASC):
        try:
            api_params = filters.model_dump(exclude_none=True) if filters else {}
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}planets", params=api_params)
                response.raise_for_status()
                data = response.json()
                                
                if sort_by:
                    data["results"] = DataSorter.apply_sorting(data["results"], sort_by, order)
                
                formatted_results = await resolve_name_fields(data["results"], ["homeworld", "films", "species", "vehicles", "starships"])
                
                return formatted_results
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

async def get_planets(self, planet_id: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}planets/{planet_id}")
                response.raise_for_status()
                data = response.json()
                
                formatted_results = await resolve_name_fields(data["results"], ["homeworld", "films", "species", "vehicles", "starships"])
                
                return formatted_results
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))