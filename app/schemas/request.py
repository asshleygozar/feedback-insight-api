from pydantic import BaseModel

class LikertScale(BaseModel):
    question: str
    points: int

class LikertScaleWithWeight(BaseModel):
    weight: int
    likert_score: LikertScale

class FeedbackRequest(BaseModel):
    id: str
    open_ended_answer: str
    likert_scale: LikertScaleWithWeight

class BatchFeedbackRequest(BaseModel):
    feedbacks: list[FeedbackRequest] 