import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

load_dotenv()

# HTTPBearer para autenticação via token Bearer
security = HTTPBearer()


class AuthService:
    async def generate_token(self):
        payload = {
            "sub": "starwars_api_user",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=1),
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
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
