from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from starwars_api.main import app


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
            "starwars_api.routes.auth_router.cache_warmup_service.warm_up_cache"
        ) as mock_warmup:
            mock_warmup.return_value = mock_result

            response = client.post("/auth/warm-cache")

            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Cache warmed successfully"
            assert "cached_endpoints" in data
            assert "total_cached_items" in data

    def test_warm_cache_failure(self, client):
        mock_result = {"message": "Cache warming failed", "error": "Connection error"}

        with patch(
            "starwars_api.routes.auth_router.cache_warmup_service.warm_up_cache"
        ) as mock_warmup:
            mock_warmup.return_value = mock_result

            response = client.post("/auth/warm-cache")

            assert (
                response.status_code == 200
            )  # Endpoint não falha, retorna erro na resposta
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

    @pytest.fixture
    def mock_auth(self):
        with patch("starwars_api.routes.swapi_router.get_current_user") as mock:
            mock.return_value = {"sub": "starwars_api_user", "role": "user"}
            yield mock

    def test_list_people_success(self, client, valid_token, mock_auth):
        mock_people_data = [
            {"name": "Luke Skywalker", "height": "172"},
            {"name": "C-3PO", "height": "167"},
        ]

        with patch(
            "starwars_api.routes.swapi_router.swapi_service.list_people"
        ) as mock_list:
            mock_list.return_value = mock_people_data

            response = client.get(
                "/api/v1/swapi/people", headers={"Authorization": valid_token}
            )

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["name"] == "Luke Skywalker"

    def test_list_people_with_filters(self, client, valid_token, mock_auth):
        mock_people_data = [{"name": "Luke Skywalker", "height": "172"}]

        with patch(
            "starwars_api.routes.swapi_router.swapi_service.list_people"
        ) as mock_list:
            mock_list.return_value = mock_people_data

            response = client.get(
                "/api/v1/swapi/people?name=Luke", headers={"Authorization": valid_token}
            )

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["name"] == "Luke Skywalker"

    def test_get_people_success(self, client, valid_token, mock_auth):
        mock_person_data = {"name": "Luke Skywalker", "height": "172"}

        with patch(
            "starwars_api.routes.swapi_router.swapi_service.get_people"
        ) as mock_get:
            mock_get.return_value = mock_person_data

            response = client.get(
                "/api/v1/swapi/people/1", headers={"Authorization": valid_token}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["name"] == "Luke Skywalker"

    def test_list_films_success(self, client, valid_token, mock_auth):
        mock_films_data = [
            {"title": "A New Hope", "episode_id": 4},
            {"title": "The Empire Strikes Back", "episode_id": 5},
        ]

        with patch(
            "starwars_api.routes.swapi_router.swapi_service.list_films"
        ) as mock_list:
            mock_list.return_value = mock_films_data

            response = client.get(
                "/api/v1/swapi/people", headers={"Authorization": valid_token}
            )

            assert response.status_code == 200

    def test_get_films_success(self, client, valid_token, mock_auth):
        mock_film_data = {"title": "A New Hope", "episode_id": 4}

        with patch(
            "starwars_api.routes.swapi_router.swapi_service.get_films"
        ) as mock_get:
            mock_get.return_value = mock_film_data

            response = client.get(
                "/api/v1/swapi/films/1", headers={"Authorization": valid_token}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["title"] == "A New Hope"

    def test_list_starships_success(self, client, valid_token, mock_auth):
        mock_starships_data = [{"name": "X-wing", "model": "T-65 X-wing"}]

        with patch(
            "starwars_api.routes.swapi_router.swapi_service.list_starships"
        ) as mock_list:
            mock_list.return_value = mock_starships_data

            response = client.get(
                "/api/v1/swapi/starships", headers={"Authorization": valid_token}
            )

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 1
            assert data[0]["name"] == "X-wing"

    def test_get_starships_success(self, client, valid_token, mock_auth):
        mock_starship_data = {"name": "X-wing", "model": "T-65 X-wing"}

        with patch(
            "starwars_api.routes.swapi_router.swapi_service.get_starships"
        ) as mock_get:
            mock_get.return_value = mock_starship_data

            response = client.get(
                "/api/v1/swapi/starships/12", headers={"Authorization": valid_token}
            )

            assert response.status_code == 200
            data = response.json()
            assert data["name"] == "X-wing"

    def test_list_vehicles_success(self, client, valid_token, mock_auth):
        mock_vehicles_data = [{"name": "Sand Crawler", "model": "Digger Crawler"}]

        with patch(
            "starwars_api.routes.swapi_router.swapi_service.list_vehicles"
        ) as mock_list:
            mock_list.return_value = mock_vehicles_data

            response = client.get(
                "/api/v1/swapi/vehicles", headers={"Authorization": valid_token}
            )

            assert response.status_code == 200

    def test_list_species_success(self, client, valid_token, mock_auth):
        mock_species_data = [{"name": "Human", "classification": "mammal"}]

        with patch(
            "starwars_api.routes.swapi_router.swapi_service.list_species"
        ) as mock_list:
            mock_list.return_value = mock_species_data

            response = client.get(
                "/api/v1/swapi/species", headers={"Authorization": valid_token}
            )

            assert response.status_code == 200

    def test_list_planets_success(self, client, valid_token, mock_auth):
        mock_planets_data = [{"name": "Tatooine", "climate": "arid"}]

        with patch(
            "starwars_api.routes.swapi_router.swapi_service.list_planets"
        ) as mock_list:
            mock_list.return_value = mock_planets_data

            response = client.get(
                "/api/v1/swapi/planets", headers={"Authorization": valid_token}
            )

            assert response.status_code == 200

    def test_unauthorized_access(self, client):
        response = client.get("/api/v1/swapi/people")

        assert response.status_code in [
            401,
            403,
            422,
        ]

    def test_invalid_token_access(self, client):
        invalid_token = "Bearer invalid_token"

        with patch("starwars_api.routes.swapi_router.get_current_user") as mock_auth:
            mock_auth.side_effect = Exception("Invalid token")

            response = client.get(
                "/api/v1/swapi/people", headers={"Authorization": invalid_token}
            )

            assert response.status_code >= 400
