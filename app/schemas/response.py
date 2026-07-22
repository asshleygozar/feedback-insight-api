from enum import Enum
from pydantic import BaseModel


class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class FeedbackResponse(BaseModel):
    sentiment: Sentiment
    summary: str
    top_praises: list[str]
    top_concerns: list[str]
