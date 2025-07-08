import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from starwars_api.enums.order_enum import Order
from starwars_api.util.naming import url_to_name
from starwars_api.util.resolve_name_fields import resolve_name_fields
from starwars_api.util.sorting import DataSorter


class TestUrlToName:
    @pytest.mark.asyncio
    async def test_url_to_name_cache_hit_name_cache(self):
        urls = ["https://swapi.info/api/people/1"]

        mock_cache = AsyncMock()
        mock_cache.get.side_effect = ["Luke Skywalker"]

        with patch("starwars_api.util.naming.redis_cache", mock_cache):
            result = await url_to_name(urls)

        assert result == ["Luke Skywalker"]
        mock_cache.get.assert_called_with("name:https://swapi.info/api/people/1")

    @pytest.mark.asyncio
    async def test_url_to_name_cache_hit_data_cache(self):
        urls = ["https://swapi.info/api/people/1"]
        cached_data = {"name": "Luke Skywalker", "height": "172"}

        mock_cache = AsyncMock()
        mock_cache.get.side_effect = [
            None,
            json.dumps(cached_data).encode("utf-8"),
        ]

        with patch(
            "starwars_api.util.naming.FastAPICache.get_backend", return_value=mock_cache
        ):
            result = await url_to_name(urls)

        assert result == ["Luke Skywalker"]
        assert mock_cache.set.call_count >= 1

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

        with patch(
            "starwars_api.util.naming.FastAPICache.get_backend", return_value=mock_cache
        ):
            with patch("httpx.AsyncClient", return_value=mock_client):
                result = await url_to_name(urls)

        assert result == ["Luke Skywalker"]
        mock_client.get.assert_called_once_with(urls[0])
        assert mock_cache.set.call_count >= 2

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

        with patch(
            "starwars_api.util.naming.FastAPICache.get_backend", return_value=mock_cache
        ):
            with patch("httpx.AsyncClient", return_value=mock_client):
                result = await url_to_name(urls)

        assert result == ["A New Hope"]

    @pytest.mark.asyncio
    async def test_url_to_name_api_error(self):
        urls = ["https://swapi.info/api/people/999"]

        mock_cache = AsyncMock()
        mock_cache.get.return_value = None

        mock_response = MagicMock()
        mock_response.status_code = 404

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response

        with patch(
            "starwars_api.util.naming.FastAPICache.get_backend", return_value=mock_cache
        ):
            with patch("httpx.AsyncClient", return_value=mock_client):
                result = await url_to_name(urls)

        assert result == [None]

    @pytest.mark.asyncio
    async def test_url_to_name_fallback_no_cache(self):
        urls = ["https://swapi.info/api/people/1"]
        api_data = {"name": "Luke Skywalker"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = api_data

        mock_client = AsyncMock()
        mock_client.get.return_value = mock_response

        with patch(
            "starwars_api.util.naming.FastAPICache.get_backend",
            side_effect=Exception("Cache error"),
        ):
            with patch("httpx.AsyncClient", return_value=mock_client):
                result = await url_to_name(urls)

        assert result == ["Luke Skywalker"]

    @pytest.mark.asyncio
    async def test_url_to_name_multiple_urls(self):
        urls = ["https://swapi.info/api/people/1", "https://swapi.info/api/films/1"]

        mock_cache = AsyncMock()
        mock_cache.get.return_value = None

        people_data = {"name": "Luke Skywalker"}
        film_data = {"title": "A New Hope"}

        mock_responses = [
            MagicMock(status_code=200, json=lambda: people_data),
            MagicMock(status_code=200, json=lambda: film_data),
        ]

        mock_client = AsyncMock()
        mock_client.get.side_effect = mock_responses

        with patch(
            "starwars_api.util.naming.FastAPICache.get_backend", return_value=mock_cache
        ):
            with patch("httpx.AsyncClient", return_value=mock_client):
                result = await url_to_name(urls)

        assert result == ["Luke Skywalker", "A New Hope"]
        assert mock_client.get.call_count == 2


class TestDataSorter:
    def test_sort_ascending(self):
        data = [
            {"name": "C-3PO", "height": "167"},
            {"name": "Luke Skywalker", "height": "172"},
            {"name": "R2-D2", "height": "96"},
        ]

        result = DataSorter.sort(data, "name", Order.ASC)

        assert len(result) == 3
        assert result[0]["name"] == "C-3PO"
        assert result[1]["name"] == "Luke Skywalker"
        assert result[2]["name"] == "R2-D2"

    def test_sort_descending(self):
        data = [
            {"name": "C-3PO", "height": "167"},
            {"name": "Luke Skywalker", "height": "172"},
            {"name": "R2-D2", "height": "96"},
        ]

        result = DataSorter.sort(data, "name", Order.DESC)

        assert len(result) == 3
        assert result[0]["name"] == "R2-D2"
        assert result[1]["name"] == "Luke Skywalker"
        assert result[2]["name"] == "C-3PO"

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

    def test_sort_missing_field(self):
        data = [{"name": "C-3PO"}, {"name": "Luke Skywalker"}]

        result = DataSorter.sort(data, "nonexistent_field", Order.ASC)

        assert len(result) == 2

    def test_sort_empty_list(self):
        data = []

        result = DataSorter.sort(data, "name", Order.ASC)

        assert result == []

    def test_sort_single_item(self):
        data = [{"name": "Luke Skywalker", "height": "172"}]

        result = DataSorter.sort(data, "name", Order.ASC)

        assert len(result) == 1
        assert result[0]["name"] == "Luke Skywalker"


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

        with patch(
            "starwars_api.util.resolve_name_fields.url_to_name"
        ) as mock_url_to_name:
            mock_url_to_name.side_effect = [
                ["Tatooine"],  # homeworld
                ["A New Hope", "The Empire Strikes Back"],  # films
            ]

            result = await resolve_name_fields(item, fields_to_resolve)

        assert result["name"] == "Luke Skywalker"
        assert result["homeworld"] == "Tatooine"
        assert result["films"] == ["A New Hope", "The Empire Strikes Back"]
        assert mock_url_to_name.call_count == 2

    @pytest.mark.asyncio
    async def test_resolve_name_fields_no_urls(self):
        item = {"name": "Luke Skywalker", "height": "172", "mass": "77"}

        fields_to_resolve = ["homeworld", "films"]

        result = await resolve_name_fields(item, fields_to_resolve)

        # Item deve permanecer inalterado
        assert result == item

    @pytest.mark.asyncio
    async def test_resolve_name_fields_mixed_fields(self):
        item = {
            "name": "Luke Skywalker",
            "homeworld": "https://swapi.info/api/planets/1",
            "height": "172",
            "films": [],  # Lista vazia
        }

        fields_to_resolve = ["homeworld", "films", "height"]

        with patch(
            "starwars_api.util.resolve_name_fields.url_to_name"
        ) as mock_url_to_name:
            mock_url_to_name.return_value = ["Tatooine"]

            result = await resolve_name_fields(item, fields_to_resolve)

        assert result["name"] == "Luke Skywalker"
        assert result["homeworld"] == "Tatooine"
        assert result["height"] == "172"
        assert result["films"] == []
        mock_url_to_name.assert_called_once()

    @pytest.mark.asyncio
    async def test_resolve_name_fields_empty_fields_list(self):
        item = {
            "name": "Luke Skywalker",
            "homeworld": "https://swapi.info/api/planets/1",
        }

        fields_to_resolve = []

        result = await resolve_name_fields(item, fields_to_resolve)

        assert result == item
