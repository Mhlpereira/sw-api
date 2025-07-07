import json
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
from fastapi import HTTPException

from starwars_api.enums.order_enum import Order
from starwars_api.routes.dto import PeopleFilterDto
from starwars_api.services.swapi_service import ENDPOINT_FIELDS_MAP, SwapiService


class TestSwapiService:
    @pytest.fixture
    def swapi_service(self):
        return SwapiService()

    @pytest.fixture
    def mock_redis_cache(self):
        mock_cache = AsyncMock()
        return mock_cache

    @pytest.fixture
    def sample_people_data(self):
        return [
            {
                "name": "Luke Skywalker",
                "height": "172",
                "homeworld": "https://swapi.info/api/planets/1",
                "films": ["https://swapi.info/api/films/1"],
                "url": "https://swapi.info/api/people/1",
            },
            {
                "name": "C-3PO",
                "height": "167",
                "homeworld": "https://swapi.info/api/planets/1",
                "films": ["https://swapi.info/api/films/1"],
                "url": "https://swapi.info/api/people/2",
            },
        ]

    @pytest.mark.asyncio
    async def test_get_cache_key_simple(self, swapi_service):
        key = await swapi_service._get_cache_key("people")
        assert key == "people"

    @pytest.mark.asyncio
    async def test_get_cache_key_with_id(self, swapi_service):
        key = await swapi_service._get_cache_key("people", "1")
        assert key == "people:1"

    @pytest.mark.asyncio
    async def test_get_cache_key_with_filters(self, swapi_service):
        filters = PeopleFilterDto(name="Luke")
        key = await swapi_service._get_cache_key("people", None, filters)
        expected_filter = json.dumps({"name": "Luke"}, sort_keys=True)
        assert key == f"people:{expected_filter}"

    @pytest.mark.asyncio
    async def test_make_request_cache_hit(self, swapi_service, mock_redis_cache):
        cached_data = {"name": "Luke Skywalker"}
        mock_redis_cache.get.return_value = cached_data

        with patch("starwars_api.services.swapi_service.redis_cache", mock_redis_cache):
            result = await swapi_service._make_request("people", "1")

            assert result == cached_data
            mock_redis_cache.get.assert_called_once()
            mock_redis_cache.set.assert_not_called()

    @pytest.mark.asyncio
    async def test_make_request_cache_miss(self, swapi_service, mock_redis_cache):
        api_data = {"name": "Luke Skywalker"}
        mock_redis_cache.get.return_value = None

        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = api_data

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response

        with patch("starwars_api.services.swapi_service.redis_cache", mock_redis_cache):
            with patch("httpx.AsyncClient", return_value=mock_client):
                result = await swapi_service._make_request("people", "1")

                assert result == api_data
                mock_redis_cache.get.assert_called_once()
                mock_redis_cache.set.assert_called_once()
                mock_client.get.assert_called_once_with(
                    "https://swapi.info/api/people/1", params={}
                )

    @pytest.mark.asyncio
    async def test_make_request_with_filters(self, swapi_service, mock_redis_cache):
        mock_redis_cache.get.return_value = None

        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
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

    @pytest.mark.asyncio
    async def test_process_response_single_item(self, swapi_service):
        data = {
            "name": "Luke Skywalker",
            "homeworld": "https://swapi.info/api/planets/1",
        }

        with patch(
            "starwars_api.services.swapi_service.resolve_name_fields"
        ) as mock_resolve:
            mock_resolve.return_value = data

            result = await swapi_service._process_response(data, "people")

            assert result == data
            mock_resolve.assert_called_once_with(data, ENDPOINT_FIELDS_MAP["people"])

    @pytest.mark.asyncio
    async def test_process_response_list_with_sorting(
        self, swapi_service, sample_people_data
    ):
        with patch("starwars_api.services.swapi_service.DataSorter.sort") as mock_sort:
            with patch(
                "starwars_api.services.swapi_service.resolve_name_fields"
            ) as mock_resolve:
                mock_sort.return_value = sample_people_data
                mock_resolve.side_effect = (
                    lambda x, _: x
                )  # Retorna o item sem modificação

                result = await swapi_service._process_response(
                    sample_people_data, "people", "name", Order.ASC
                )

                assert len(result) == 2
                mock_sort.assert_called_once_with(sample_people_data, "name", Order.ASC)
                assert mock_resolve.call_count == 2

    @pytest.mark.asyncio
    async def test_list_resources_cache_hit(
        self, swapi_service, mock_redis_cache, sample_people_data
    ):
        mock_redis_cache.get.return_value = sample_people_data

        with patch("starwars_api.services.swapi_service.redis_cache", mock_redis_cache):
            result = await swapi_service.list_resources("people")

            assert result == sample_people_data
            mock_redis_cache.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_resources_cache_miss(
        self, swapi_service, mock_redis_cache, sample_people_data
    ):
        mock_redis_cache.get.return_value = None

        with patch.object(
            swapi_service, "_make_request", return_value=sample_people_data
        ):
            with patch.object(
                swapi_service, "_process_response", return_value=sample_people_data
            ):
                with patch(
                    "starwars_api.services.swapi_service.redis_cache", mock_redis_cache
                ):
                    result = await swapi_service.list_resources("people")

                    assert result == sample_people_data
                    mock_redis_cache.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_resources_http_error(self, swapi_service):
        mock_response = MagicMock()
        mock_response.status_code = 404

        http_error = httpx.HTTPStatusError(
            "Not found", request=MagicMock(), response=mock_response
        )

        with patch.object(swapi_service, "_make_request", side_effect=http_error):
            with pytest.raises(HTTPException) as exc_info:
                await swapi_service.list_resources("people")

            assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_get_resource_cache_hit(self, swapi_service, mock_redis_cache):
        cached_data = {"name": "Luke Skywalker"}
        mock_redis_cache.get.return_value = cached_data

        with patch("starwars_api.services.swapi_service.redis_cache", mock_redis_cache):
            result = await swapi_service.get_resource("people", "1")

            assert result == cached_data
            mock_redis_cache.get.assert_called_once_with("people_1_processed")

    @pytest.mark.asyncio
    async def test_get_resource_cache_miss(self, swapi_service, mock_redis_cache):
        resource_data = {"name": "Luke Skywalker"}
        mock_redis_cache.get.return_value = None

        with patch.object(swapi_service, "_make_request", return_value=resource_data):
            with patch.object(
                swapi_service, "_process_response", return_value=resource_data
            ):
                with patch(
                    "starwars_api.services.swapi_service.redis_cache", mock_redis_cache
                ):
                    result = await swapi_service.get_resource("people", "1")

                    assert result == resource_data
                    mock_redis_cache.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_people(self, swapi_service):
        filters = PeopleFilterDto(name="Luke")

        with patch.object(
            swapi_service, "list_resources", return_value=[]
        ) as mock_list:
            result = await swapi_service.list_people(filters, "name", Order.DESC)

            mock_list.assert_called_once_with("people", filters, "name", Order.DESC)
            assert result == []

    @pytest.mark.asyncio
    async def test_get_people(self, swapi_service):
        person_data = {"name": "Luke Skywalker"}

        with patch.object(
            swapi_service, "get_resource", return_value=person_data
        ) as mock_get:
            result = await swapi_service.get_people("1")

            mock_get.assert_called_once_with("people", "1")
            assert result == person_data

    @pytest.mark.asyncio
    async def test_list_films(self, swapi_service):
        with patch.object(
            swapi_service, "list_resources", return_value=[]
        ) as mock_list:
            result = await swapi_service.list_films()

            mock_list.assert_called_once_with("films", None, None, Order.ASC)
            assert result == []

    @pytest.mark.asyncio
    async def test_get_films(self, swapi_service):
        film_data = {"title": "A New Hope"}

        with patch.object(
            swapi_service, "get_resource", return_value=film_data
        ) as mock_get:
            result = await swapi_service.get_films("1")

            mock_get.assert_called_once_with("films", "1")
            assert result == film_data

    @pytest.mark.asyncio
    async def test_endpoint_fields_map_coverage(self):
        expected_endpoints = [
            "people",
            "films",
            "starships",
            "vehicles",
            "species",
            "planets",
        ]

        for endpoint in expected_endpoints:
            assert endpoint in ENDPOINT_FIELDS_MAP
            assert isinstance(ENDPOINT_FIELDS_MAP[endpoint], list)
            assert len(ENDPOINT_FIELDS_MAP[endpoint]) > 0
