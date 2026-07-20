import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1 import v1_router
from app.core import settings
from app.core import load_ai_client, ai_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_ai_client()
    yield

app = FastAPI(title=settings.APP_NAME, version="1.0.0", description="AI Powered API for feedback insights", lifespan=lifespan)

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

