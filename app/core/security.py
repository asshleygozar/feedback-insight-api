from fastapi.security import APIKeyHeader
from fastapi import HTTPException, Depends
from app.core import settings

header_scheme = APIKeyHeader(name="X-API-Key", auto_error=True)


class Authentication:
    def verify_api_key(self, api_key: str = Depends(header_scheme)):
        if api_key != settings.API_SECRET_KEY:
            raise HTTPException(status_code=401, detail="Invalid API Key")
        return api_key


authentication = Authentication()
