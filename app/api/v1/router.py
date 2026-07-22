from fastapi import APIRouter
from .routers import feedbacks_router

api_router = APIRouter()

api_router.include_router(
    feedbacks_router, prefix="/feedbacks", tags=["Feedbacks"]
)  # Feedback routers
