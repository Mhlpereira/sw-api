from typing import Optional

import httpx
from fastapi import HTTPException
from pydantic import BaseModel

from starwars_api.enums.order_enum import Order
from starwars_api.routes.dto import (
    FilmsFilterDto,
    PeopleFilterDto,
    PlanetsFilterDto,
    SpeciesFilterDto,
    StarshipsFilterDto,
    VehiclesFilterDto,
)
from starwars_api.util import DataSorter, resolve_name_fields

# Mapeamento de campos para resolução de nomes por endpoint
ENDPOINT_FIELDS_MAP = {
    "people": ["homeworld", "films", "species", "vehicles", "starships"],
    "films": ["characters", "planets", "starships", "vehicles", "species"],
    "starships": ["pilots", "films"],
    "vehicles": ["pilots", "films"],
    "species": ["homeworld", "people", "films"],
    "planets": ["residents", "films"],
}


class SwapiService:
    def __init__(self):
        self.api_url = "https://swapi.info/api/"

    async def _make_request(
        self,
        endpoint: str,
        resource_id: Optional[str] = None,
        filters: Optional[BaseModel] = None,
    ):
        """Método privado para fazer requisições genéricas"""
        api_params = filters.model_dump(exclude_none=True) if filters else {}
        url = f"{self.api_url}{endpoint}"
        if resource_id:
            url = f"{url}/{resource_id}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=api_params)
            response.raise_for_status()
            return response.json()

    async def _process_response(
        self,
        data,
        endpoint: str,
        sort_by: Optional[str] = None,
        order: Order = Order.ASC,
    ):
        """Processa a resposta da API"""
        if isinstance(data, list):
            if sort_by:
                data = DataSorter.sort(data, sort_by, order)

            formatted_results = []
            for item in data:
                formatted_item = await resolve_name_fields(
                    item, ENDPOINT_FIELDS_MAP[endpoint]
                )
                formatted_results.append(formatted_item)

            return formatted_results
        else:
            return await resolve_name_fields(data, ENDPOINT_FIELDS_MAP[endpoint])

    async def list_resources(
        self,
        endpoint: str,
        filters: Optional[BaseModel] = None,
        sort_by: Optional[str] = None,
        order: Order = Order.ASC,
    ):
        """Método genérico para listar recursos"""
        try:
            data = await self._make_request(endpoint, None, filters)
            return await self._process_response(data, endpoint, sort_by, order)
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

    async def get_resource(self, endpoint: str, resource_id: str):
        """Método genérico para obter um recurso específico"""
        try:
            data = await self._make_request(endpoint, resource_id)
            return await self._process_response(data, endpoint)
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

    async def list_people(
        self,
        filters: Optional[PeopleFilterDto] = None,
        sort_by: Optional[str] = None,
        order: Order = Order.ASC,
    ):
        return await self.list_resources("people", filters, sort_by, order)

    async def get_people(self, person_id: str):
        return await self.get_resource("people", person_id)

    async def list_films(
        self,
        filters: Optional[FilmsFilterDto] = None,
        sort_by: Optional[str] = None,
        order: Order = Order.ASC,
    ):
        return await self.list_resources("films", filters, sort_by, order)

    async def get_films(self, film_id: str):
        return await self.get_resource("films", film_id)

    async def list_starships(
        self,
        filters: Optional[StarshipsFilterDto] = None,
        sort_by: Optional[str] = None,
        order: Order = Order.ASC,
    ):
        return await self.list_resources("starships", filters, sort_by, order)

    async def get_starships(self, starship_id: str):
        return await self.get_resource("starships", starship_id)

    async def list_vehicles(
        self,
        filters: Optional[VehiclesFilterDto] = None,
        sort_by: Optional[str] = None,
        order: Order = Order.ASC,
    ):
        return await self.list_resources("vehicles", filters, sort_by, order)

    async def get_vehicles(self, vehicle_id: str):
        return await self.get_resource("vehicles", vehicle_id)

    async def list_species(
        self,
        filters: Optional[SpeciesFilterDto] = None,
        sort_by: Optional[str] = None,
        order: Order = Order.ASC,
    ):
        return await self.list_resources("species", filters, sort_by, order)

    async def get_species(self, species_id: str):
        return await self.get_resource("species", species_id)

    async def list_planets(
        self,
        filters: Optional[PlanetsFilterDto] = None,
        sort_by: Optional[str] = None,
        order: Order = Order.ASC,
    ):
        return await self.list_resources("planets", filters, sort_by, order)

    async def get_planets(self, planet_id: str):
        return await self.get_resource("planets", planet_id)
