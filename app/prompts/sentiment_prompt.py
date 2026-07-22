from app.schemas import FeedbackRequest, BatchFeedbackRequest


def build_single_sentiment_prompt(data: FeedbackRequest):
    prompt = f"""

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
        """
    return prompt


def build_batch_sentiment_prompt(data: BatchFeedbackRequest):
    prompt = f"""

        Here are the batch feedback responses {data}

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
        """
    return prompt
