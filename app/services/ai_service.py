from app.core import ai_client
from app.schemas import FeedbackRequest, FeedbackResponse
from fastapi import HTTPException
from google.genai import types

class AIService:
    # For analyzing single object feedback
    def analyze_feedback(self, data: FeedbackRequest) -> FeedbackResponse:
        if ai_client is None:
            raise HTTPException(status_code=500, detail="AI client is not initialized.")

        prompt = f'''

        Here are the feedback responses {data}

        You are a specialized in feedback sentiment analysis. 
        Your objective is to analyze both quantitative (Likert scale) ratings and qualitative (open-ended text) feedback.
        Given the feedback context, generate a JSON response summarizing the sentiments.

        Rules:
        1. "sentiment" must be exactly one of: "Positive", "Negative", "Neutral", or "Mixed"
        2. "summary" should be a 2-3 sentence overview that captures the essence of the feedback, highlighting key points and overall sentiment.
        3. "top_praises" should be the top 5 positive aspects or strengths mentioned in open ended answer and score on likert scale, if any. If there are no praises, return an empty list.
        4. "top_concerns" should be the top 5 negative aspects or weaknesses mentioned in open ended answer and score on likert scale, if any. If there are no concerns, return an empty list.
        5. Provide only the raw and valid JSON matching this interface:
        {{
        
            "sentiment": "Positive" | "Negative" | "Neutral" | "Mixed",
            "summary": "string",
            "top_praises": list["string"],
            "top_concerns": list["string"]
        }}
        '''

        response = ai_client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=FeedbackResponse
            )
        )

        if response.text is None:
            raise HTTPException(status_code=500, detail="Failed to generate response from AI model.")
       
        return FeedbackResponse.model_validate_json(response.text)