from fastapi import FastAPI, Request, status, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from google.genai.errors import APIError as GeminiAPIError
from contextlib import asynccontextmanager
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.api.v1 import v1_router
from app.core import settings
from app.core import load_ai_client, ai_client, authentication, limiter
import uvicorn
import http


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_ai_client()
    yield


app = FastAPI(title=settings.APP_NAME, version="1.0.0", description="AI Powered API for feedback insights", lifespan=lifespan, dependencies=[Depends(authentication.verify_api_key)])

# For accessing rate limit to routers
app.state.limiter = limiter

# For automatic injection of X-RateLimit headers to the responses
app.add_middleware(SlowAPIMiddleware)

# Rate limiter exception handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "type":"about:blank",
            "title":"Too Many Requests",
            "status": status.HTTP_429_TOO_MANY_REQUESTS,
            "detail": "You have exceeded the rate limit. Please try again later.",
            "instance": request.url.path
        }
    )

# Global exception handler for Gemini API Errors
@app.exception_handler(GeminiAPIError)
async def gemini_exception_handler(request: Request, exc: GeminiAPIError):
    upstream_status = getattr(exc, 'code', 500)
    detail = getattr(exc, 'message', 'An error occurred while communicating with the Gemini API.')

    return JSONResponse(
        status_code=upstream_status,
        content={
            "type": "about:blank",
            "title": "Gemini Service Error",
            "status": upstream_status,
            "detail": detail,
            "instance": request.url.path
        }
    )


# Global exception handler for HTTP Exceptions such as 400 plus and 500 plus errors
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    try:
        title = http.HTTPStatus(exc.status_code).phrase
    except ValueError:
        title = "An error occured"

    error_details = {
        "type": "about:blank",
        "title": title,
        "status": exc.status_code,
        "detail": str(exc.detail),
        "instance": request.url.path
    }
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_details
    )

# Global exception handler for request validation errors | 422 Unprocess entity
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    formatted_errors = []
    
    for error in errors:
        loc = error.get("loc", [])

        if len(loc) > 1:
            field = ".".join(str(x) for x in loc[1:])
        else:
            field = str(loc[0] if loc else "unknown")
        
        formatted_errors.append({
            "field": field,
            "message": error.get("msg"),
            "code": error.get("type")
        })

    # follows the RFC 7807 standard for HTTP API ERRORS
    error_details = {
        "type": "about:blank",
        "title": "Validation Error",
        "status": status.HTTP_422_UNPROCESSABLE_CONTENT,
        "detail": "Your request payload contain validation errors.",
        "errors": formatted_errors
    }
    
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content=error_details)


app.include_router(v1_router, prefix="/api/v1")

@app.get('/health')
def health():
    if ai_client is None:
        return {"status": "unhealthy", "ai_client_loaded": False}
    return {"status": "healthy", "ai_client_loaded": True}



if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,  
        reload=True
    )

