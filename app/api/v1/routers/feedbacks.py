from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from app.schemas import FeedbackRequest, FeedbackResponse
from app.services import AIService

router = APIRouter()

@router.post('/analyze')
def analyze(data: FeedbackRequest, ai_service: AIService = Depends()) -> FeedbackResponse:
    try:
        response = ai_service.analyze_feedback(data)

        if response is None:
            raise HTTPException(status_code=500, detail="Failed to analyze feedback.")

        return response
    except Exception as error:
        raise HTTPException(status_code=500, detail='An unexpected error occured while analyzing your feedback.')
