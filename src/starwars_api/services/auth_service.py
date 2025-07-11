import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

load_dotenv()

security = HTTPBearer()


class AuthService:
    async def generate_token(self):
        now = datetime.now(timezone.utc)
        exp = now + timedelta(hours=1)
        payload = {
            "sub": "starwars_api_user",
            "iat": int(now.timestamp()),
            "exp": int(exp.timestamp()), 
            "role": "user",
        }

        token = jwt.encode(
            payload, os.getenv("JWT_SECRET_KEY", "your_secret_key"), algorithm="HS256"
        )

        return {"access_token": token, "token_type": "bearer"}


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        token = credentials.credentials
        payload = jwt.decode(
            token, os.getenv("JWT_SECRET_KEY", "your_secret_key"), algorithms=["HS256"]
        )

        if payload.get("exp") < int(datetime.utcnow().timestamp()):
            raise HTTPException(
                status_code=401,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
