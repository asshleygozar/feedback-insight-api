from app.core import ai_client
from app.schemas import FeedbackRequest, BatchFeedbackRequest, FeedbackResponse
from app.prompts import build_single_sentiment_prompt, build_batch_sentiment_prompt
from fastapi import HTTPException
from google.genai import types


class AIService:
    # For analyzing single object feedback
    def analyze_feedback(self, data: FeedbackRequest) -> FeedbackResponse:
        if ai_client is None:
            raise HTTPException(status_code=500, detail="AI client is not initialized.")

        prompt = build_single_sentiment_prompt(data)

        response = ai_client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json", response_schema=FeedbackResponse
            ),
        )

        if response.text is None:
            raise HTTPException(
                status_code=500, detail="Failed to generate response from AI model."
            )

        return FeedbackResponse.model_validate_json(response.text)

    # For analyzing batch of feedbacks
    def batch_analyze_feedbacks(self, data: BatchFeedbackRequest) -> FeedbackResponse:
        if ai_client is None:
            raise HTTPException(status_code=500, detail="AI client is not initialized.")

        prompt = build_batch_sentiment_prompt(data)

        response = ai_client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json", response_schema=FeedbackResponse
            ),
        )

        if response.text is None:
            raise HTTPException(
                status_code=500, detail="Failed to generate response from AI model."
            )

        return FeedbackResponse.model_validate_json(response.text)
