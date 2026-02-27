from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

from app.config import get_settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    settings = get_settings()
    valid_keys = [k.strip() for k in settings.VALID_API_KEYS.split(",") if k.strip()]
    if not api_key or api_key not in valid_keys:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")
    return api_key
