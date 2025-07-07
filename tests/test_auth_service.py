from datetime import datetime, timezone
from unittest.mock import patch

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import JWTError

from starwars_api.services.auth_service import AuthService, get_current_user


class TestAuthService:
    @pytest.fixture
    def auth_service(self):
        return AuthService()

    @pytest.mark.asyncio
    async def test_generate_token_success(self, auth_service):
        with patch("starwars_api.services.auth_service.datetime") as mock_datetime:
            mock_now = datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
            mock_datetime.utcnow.return_value = mock_now

            with patch(
                "starwars_api.services.auth_service.jwt.encode",
                return_value="mocked_token",
            ):
                result = await auth_service.generate_token()

                assert "access_token" in result
                assert "token_type" in result
                assert result["token_type"] == "bearer"
                assert result["access_token"] == "mocked_token"


class TestGetCurrentUser:
    @pytest.mark.asyncio
    async def test_get_current_user_valid_token(self):
        payload = {
            "sub": "starwars_api_user",
            "iat": datetime.now(timezone.utc).timestamp(),
            "exp": datetime.now(timezone.utc).timestamp() + 3600,
            "role": "user",
        }

        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer", credentials="valid_token"
        )

        with patch(
            "starwars_api.services.auth_service.jwt.decode", return_value=payload
        ):
            result = await get_current_user(credentials)

            assert result == payload

    @pytest.mark.asyncio
    async def test_get_current_user_invalid_token(self):
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer", credentials="invalid_token"
        )

        with patch(
            "starwars_api.services.auth_service.jwt.decode", side_effect=JWTError
        ):
            with pytest.raises(HTTPException) as exc_info:
                await get_current_user(credentials)

            assert exc_info.value.status_code == 401
            assert "Invalid authentication credentials" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_get_current_user_expired_token(self):
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer", credentials="expired_token"
        )

        with patch(
            "starwars_api.services.auth_service.jwt.decode", side_effect=JWTError
        ):
            with pytest.raises(HTTPException) as exc_info:
                await get_current_user(credentials)

            assert exc_info.value.status_code == 401
            assert "Invalid authentication credentials" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_get_current_user_malformed_token(self):
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer", credentials="malformed.token"
        )

        with patch(
            "starwars_api.services.auth_service.jwt.decode", side_effect=JWTError
        ):
            with pytest.raises(HTTPException) as exc_info:
                await get_current_user(credentials)

            assert exc_info.value.status_code == 401
            assert "Invalid authentication credentials" in str(exc_info.value.detail)
