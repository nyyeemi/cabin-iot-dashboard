import os

from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

API_KEY = os.environ.get("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key")


async def verify_api_key(key: str = Security(api_key_header)):
    if key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid api key",
        )
