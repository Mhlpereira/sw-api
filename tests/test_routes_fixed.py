from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from starwars_api.enums.order_enum import Order
from starwars_api.main import app
from starwars_api.routes.dto import PeopleFilterDto
from starwars_api.util import DataSorter
from starwars_api.util.naming import url_to_name
from starwars_api.util.resolve_name_fields import resolve_name_fields


class TestAuthRouter:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_authenticate_success(self, client):
        with patch(
            "starwars_api.services.auth_service.AuthService.generate_token"
        ) as mock_generate:
            mock_generate.return_value = {
                "access_token": "test_token",
                "token_type": "bearer",
            }

            response = client.post("/auth/auth")

            assert response.status_code == 201
            data = response.json()
            assert "access_token" in data
            assert "token_type" in data
            assert data["token_type"] == "bearer"

    def test_warm_cache_success(self, client):
        mock_result = {
            "message": "Cache warmed successfully",
            "cached_endpoints": {"people": 82, "films": 6},
            "total_cached_items": 88,
            "total_cached_names": 88,
        }

        with patch(
            "starwars_api.cache.warmup_service.cache_warmup_service.warm_up_cache"
        ) as mock_warmup:
            mock_warmup.return_value = mock_result

            response = client.post("/auth/warm-cache")

            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Cache warmed successfully"
            assert "cached_endpoints" in data
            assert "total_cached_items" in data


class TestSwapiRouter:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    @pytest.fixture
    def valid_token(self):
        return "Bearer valid_token_here"

    @pytest.fixture
    def mock_auth(self):
        with patch("starwars_api.services.auth_service.get_current_user") as mock:
            mock.return_value = {"sub": "starwars_api_user", "role": "user"}
            yield mock

    def test_list_people_success(self, client, valid_token, mock_auth):
        mock_people_data = [
            {"name": "Luke Skywalker", "height": "172"},
            {"name": "C-3PO", "height": "167"},
        ]

        with patch(
            "starwars_api.services.swapi_service.SwapiService.list_people"
        ) as mock_list:
            mock_list.return_value = mock_people_data

            response = client.get(
                "/api/v1/swapi/people", headers={"Authorization": valid_token}
            )

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["name"] == "Luke Skywalker"

    def test_invalid_token_access(self, client):
        invalid_token = "Bearer invalid_token"

        with patch("starwars_api.services.auth_service.get_current_user") as mock_auth:
            mock_auth.side_effect = Exception("Invalid token")

            response = client.get(
                "/api/v1/swapi/people", headers={"Authorization": invalid_token}
            )

            assert response.status_code == 500  # ou o código de erro esperado


class TestSwapiService:
    @pytest.fixture
    def swapi_service(self):
        from starwars_api.services.swapi_service import SwapiService

        return SwapiService()

    @pytest.fixture
    def mock_redis_cache(self):
        return AsyncMock()

    @pytest.mark.asyncio
    async def test_make_request_cache_miss(self, swapi_service, mock_redis_cache):
        api_data = {"name": "Luke Skywalker"}
        mock_redis_cache.get.return_value = None

        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = api_data

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response

        with patch("starwars_api.services.swapi_service.redis_cache", mock_redis_cache):
            with patch("httpx.AsyncClient", return_value=mock_client):
                result = await swapi_service._make_request("people", "1")

                assert result == api_data

    @pytest.mark.asyncio
    async def test_make_request_with_filters(self, swapi_service, mock_redis_cache):
        mock_redis_cache.get.return_value = None

        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = []

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response

        filters = PeopleFilterDto(name="Luke")

        with patch("starwars_api.services.swapi_service.redis_cache", mock_redis_cache):
            with patch("httpx.AsyncClient", return_value=mock_client):
                await swapi_service._make_request("people", None, filters)

                mock_client.get.assert_called_once_with(
                    "https://swapi.info/api/people", params={"name": "Luke"}
                )


class TestUrlToName:
    @pytest.mark.asyncio
    async def test_url_to_name_cache_miss(self):
        urls = ["https://swapi.info/api/people/1"]
        api_data = {"name": "Luke Skywalker", "height": "172"}

        mock_cache = AsyncMock()
        mock_cache.get.return_value = None

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = api_data

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response

        with patch("starwars_api.util.naming.redis_cache", mock_cache):
            with patch("httpx.AsyncClient", return_value=mock_client):
                result = await url_to_name(urls)

        assert result == ["Luke Skywalker"]

    @pytest.mark.asyncio
    async def test_url_to_name_with_title(self):
        urls = ["https://swapi.info/api/films/1"]
        api_data = {"title": "A New Hope", "episode_id": 4}

        mock_cache = AsyncMock()
        mock_cache.get.return_value = None

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = api_data

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response

        with patch("starwars_api.util.naming.redis_cache", mock_cache):
            with patch("httpx.AsyncClient", return_value=mock_client):
                result = await url_to_name(urls)

        assert result == ["A New Hope"]


class TestDataSorter:
    def test_sort_numeric_field(self):
        data = [
            {"name": "C-3PO", "height": "167"},
            {"name": "Luke Skywalker", "height": "172"},
            {"name": "R2-D2", "height": "96"},
        ]

        result = DataSorter.sort(data, "height", Order.ASC)

        assert len(result) == 3
        assert result[0]["name"] == "R2-D2"
        assert result[1]["name"] == "C-3PO"
        assert result[2]["name"] == "Luke Skywalker"

    def test_sort_string_field(self):
        data = [
            {"name": "Luke Skywalker"},
            {"name": "C-3PO"},
            {"name": "R2-D2"},
        ]

        result = DataSorter.sort(data, "name", Order.ASC)

        assert len(result) == 3
        assert result[0]["name"] == "C-3PO"


class TestResolveNameFields:
    @pytest.mark.asyncio
    async def test_resolve_name_fields_with_urls(self):
        item = {
            "name": "Luke Skywalker",
            "homeworld": "https://swapi.info/api/planets/1",
            "films": [
                "https://swapi.info/api/films/1",
                "https://swapi.info/api/films/2",
            ],
        }

        fields_to_resolve = ["homeworld", "films"]

        with patch("starwars_api.util.naming.url_to_name") as mock_url_to_name:
            mock_url_to_name.side_effect = [
                ["Tatooine"],  # para homeworld
                ["A New Hope", "The Empire Strikes Back"],  # para films
            ]

            result = await resolve_name_fields(item, fields_to_resolve)

            assert result["homeworld"] == "Tatooine"
            assert result["films"] == ["A New Hope", "The Empire Strikes Back"]

    @pytest.mark.asyncio
    async def test_resolve_name_fields_no_urls(self):
        item = {"name": "Luke Skywalker", "height": "172"}
        fields_to_resolve = ["height"]

        result = await resolve_name_fields(item, fields_to_resolve)

        assert result == item
