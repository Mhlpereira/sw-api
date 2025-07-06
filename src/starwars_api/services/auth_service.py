import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


class AuthService:
    def __init__(self, auth_url: str):
        self.auth_url = auth_url

    async def generate_token():
        payload = {
            "sub": "starwars_api_user",
            "iat": jwt.datetime.utcnow(),
            "exp": jwt.datetime.utcnow() + jwt.timedelta(hours=1),
            "role": "user"
        }
        
        token = jwt.encode(
            payload,
            os.getenv("JWT_SECRET_KEY", "your_secret_key"),
            algorithm="HS256"
            )
        
        return { "access_token": token, "token_type": "bearer" }
    
    async def authenticate(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY", algorithm="HS256"))
            return payload
        except jwt.JWTError:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )