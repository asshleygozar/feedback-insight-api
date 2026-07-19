import uvicorn
from fastapi import FastAPI, Depends
from app.api.v1 import v1_router
from app.core import settings, AppSettings


app = FastAPI(title=settings.APP_NAME, version="1.0.0", description="AI Powered API for feedback insights")

app.include_router(v1_router, prefix="/api/v1")

@app.get('/health')
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,  
        reload=True
    )

