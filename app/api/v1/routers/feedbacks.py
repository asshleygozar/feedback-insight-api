from fastapi import APIRouter, Depends, HTTPException, Request
from app.schemas import FeedbackRequest, BatchFeedbackRequest, FeedbackResponse
from app.services import AIService
from app.core import limiter
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/analyze")
@limiter.limit("5/minute")  # 5 request per minute because ai token is expensive
async def analyze(
    request: Request, data: FeedbackRequest, ai_service: AIService = Depends()
) -> FeedbackResponse:

    response = ai_service.analyze_feedback(data)

    if response is None:
        logger.error(
            f"Failed to analyze feedback for request {request.url.path} - {request.method}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail="Failed to analyze feedback.")

    return response


@router.post("/batch-analyze")
@limiter.limit("5/minute")
async def batch_analyze(
    request: Request, data: BatchFeedbackRequest, ai_service: AIService = Depends()
) -> FeedbackResponse:

    responses = ai_service.batch_analyze_feedbacks(data)

    if responses is None:
        logger.error(
            f"Failed to analyze feedbacks for request {request.url.path} - {request.method}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail="Failed to analyze feedbacks.")

    return responses
