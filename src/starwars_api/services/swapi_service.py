import httpx
from fastapi import HTTPException

class SwapiService:

    def __init__(self):
        self.api_url = "https://swapi.info/api/"
