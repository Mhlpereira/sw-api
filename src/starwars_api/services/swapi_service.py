import httpx
from fastapi import HTTPException

class SwapiService:

    def __init__(self):
        self.api_url = "https://swapi.info/api/"

async def list_people(self, filters=None):
        try:
            
            parameters = {key: value for key, value in filters.items() if value is not None}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}people", params=parameters)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        
async def get_people(self, person_id: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}people/{person_id}")
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        
async def list_films(self, filters=None):
        try:
            parameters = {key: value for key, value in filters.items() if value is not None}
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}films", params=parameters)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        
async def get_films(self, film_id: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}films/{film_id}")
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        
async def list_starships(self, filters=None):
        try:
            parameters = {key: value for key, value in filters.items() if value is not None}
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}starships", params=parameters)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        
async def get_starships(self, starship_id: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}starships/{starship_id}")
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

async def list_vehicles(self, filters=None):
        try:
            parameters = {key: value for key, value in filters.items() if value is not None}
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}vehicles", params=parameters)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        
async def get_vehicles(self, vehicle_id: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}vehicles/{vehicle_id}")
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

async def list_species(self, filters=None):
        try:
            parameters = {key: value for key, value in filters.items() if value is not None}
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}species", params=parameters)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

async def get_species(self, species_id: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}species/{species_id}")
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

async def list_planets(self, filters=None):
        try:
            parameters = {key: value for key, value in filters.items() if value is not None}
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}planets", params=parameters)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))

async def get_planets(self, planet_id: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.api_url}planets/{planet_id}")
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))