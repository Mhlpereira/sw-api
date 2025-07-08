from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from starwars_api.enums.order_enum import Order
from starwars_api.main import app
from starwars_api.util import DataSorter


class TestAuthRouter:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_authenticate_success(self, client):
        """Testa geração de token com sucesso"""
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
        """Testa warm-up do cache com sucesso"""
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

    def test_warm_cache_failure(self, client):
        """Testa warm-up do cache com falha"""
        mock_result = {"message": "Cache warming failed", "error": "Connection error"}

        with patch(
            "starwars_api.cache.warmup_service.cache_warmup_service.warm_up_cache"
        ) as mock_warmup:
            mock_warmup.return_value = mock_result

            response = client.post("/auth/warm-cache")

            assert response.status_code == 200
            data = response.json()
            assert "Cache warming failed" in data["message"]
            assert "error" in data


class TestSwapiRouter:
    @pytest.fixture
    def client(self):
        return TestClient(app)

    @pytest.fixture
    def valid_token(self):
        return "Bearer valid_token_here"

    def test_invalid_token_access(self, client):
        """Testa acesso com token inválido"""
        invalid_token = "Bearer invalid_token"

        response = client.get(
            "/api/v1/swapi/people", headers={"Authorization": invalid_token}
        )

        assert response.status_code == 401


class TestDataSorter:
    def test_sort_numeric_field(self):
        """Testa ordenação por campo numérico"""
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
        """Testa ordenação por campo de string"""
        data = [
            {"name": "Luke Skywalker"},
            {"name": "C-3PO"},
            {"name": "R2-D2"},
        ]

        result = DataSorter.sort(data, "name", Order.ASC)

        assert len(result) == 3
        assert result[0]["name"] == "C-3PO"

    def test_sort_desc_order(self):
        """Testa ordenação decrescente"""
        data = [
            {"height": "96"},
            {"height": "167"},
            {"height": "172"},
        ]

        result = DataSorter.sort(data, "height", Order.DESC)

        assert result[0]["height"] == "172"
        assert result[1]["height"] == "167"
        assert result[2]["height"] == "96"

    def test_sort_no_field(self):
        """Testa quando não há campo para ordenar"""
        data = [{"name": "Luke"}, {"name": "Leia"}]

        result = DataSorter.sort(data, None)

        assert result == data

    def test_sort_missing_field(self):
        """Testa ordenação com campo ausente"""
        data = [
            {"name": "Luke"},
            {"name": "Leia", "height": "150"},
        ]

        result = DataSorter.sort(data, "height", Order.ASC)

        assert len(result) == 2


class TestResolveNameFields:
    @pytest.mark.asyncio
    async def test_resolve_name_fields_with_urls(self):
        """Testa resolução de campos com URLs"""
        from starwars_api.util.resolve_name_fields import resolve_name_fields

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
        """Testa resolução sem URLs"""
        from starwars_api.util.resolve_name_fields import resolve_name_fields

        item = {"name": "Luke Skywalker", "height": "172"}
        fields_to_resolve = ["height"]

        result = await resolve_name_fields(item, fields_to_resolve)

        assert result == item

    @pytest.mark.asyncio
    async def test_resolve_name_fields_mixed_fields(self):
        """Testa resolução com campos mistos"""
        from starwars_api.util.resolve_name_fields import resolve_name_fields

        item = {
            "name": "Luke Skywalker",
            "homeworld": "https://swapi.info/api/planets/1",
            "height": "172",
            "films": [],
        }

        fields_to_resolve = ["homeworld", "films", "height"]

        with patch("starwars_api.util.naming.url_to_name") as mock_url_to_name:
            mock_url_to_name.side_effect = [
                ["Tatooine"],  # para homeworld
                [],  # para films (lista vazia)
            ]

            result = await resolve_name_fields(item, fields_to_resolve)

            assert result["homeworld"] == "Tatooine"
            assert result["films"] == []
            assert result["height"] == "172"

    @pytest.mark.asyncio
    async def test_resolve_name_fields_empty_fields_list(self):
        """Testa com lista de campos vazia"""
        from starwars_api.util.resolve_name_fields import resolve_name_fields

        item = {
            "name": "Luke Skywalker",
            "homeworld": "https://swapi.info/api/planets/1",
        }

        fields_to_resolve = []

        result = await resolve_name_fields(item, fields_to_resolve)

        assert result == item


class TestCacheAndConnections:
    def test_redis_connection_success(self):
        """Testa se a configuração Redis está correta"""
        import os

        from dotenv import load_dotenv

        load_dotenv()
        redis_url = os.getenv("REDIS_URL")

        assert redis_url is not None
        assert "redis://" in redis_url

    def test_jwt_secret_exists(self):
        """Testa se JWT secret está configurado"""
        import os

        from dotenv import load_dotenv

        load_dotenv()
        jwt_secret = os.getenv("JWT_SECRET_KEY")

        assert jwt_secret is not None
        assert len(jwt_secret) > 10
