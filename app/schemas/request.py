from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError


class LikertScore(BaseModel):
    question: str = Field(..., min_length=5)
    points: int

    @field_validator("points")
    def validate_points(cls, value):
        if value < 1 or value > 7:
            raise PydanticCustomError(
                "points_range_error", "Points must be between 1 and 7"
            )
        return value


class FeedbackRequest(BaseModel):
    id: str
    open_ended_answer: str
    likert_score: LikertScore

    @field_validator("open_ended_answer")
    def validate_open_ended_answer(cls, value):
        stripped_value = value.strip()

        if not stripped_value:
            raise PydanticCustomError(
                "open_ended_answer_empty", "Open-ended answer cannot be empty"
            )
        if len(stripped_value) > 700:
            raise PydanticCustomError(
                "open_ended_answer_too_long",
                "Open-ended answer cannot exceed 700 characters",
            )
        return stripped_value


class BatchFeedbackRequest(BaseModel):
    feedbacks: list[FeedbackRequest]

    # Maximum of 50 feedbacks in a single batch request only because tokens burns too fast when to many words or texts is given
    @field_validator("feedbacks")
    def validate_feedbacks(cls, value):
        if len(value) > 50:
            raise PydanticCustomError(
                "feedbacks_too_many",
                "Maximum of 50 feedbacks allowed in a single batch request",
            )
        return value
