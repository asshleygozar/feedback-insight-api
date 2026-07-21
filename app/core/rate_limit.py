from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

# Use by API key if provided, otherwise use the remote address for rate limiting to ensure consistency and accuracy
def get_by_api_key(request: Request):
    api_key = request.headers.get("X-API-Key")
    if api_key:
        return api_key
    return get_remote_address(request)

limiter = Limiter(key_func=get_by_api_key)