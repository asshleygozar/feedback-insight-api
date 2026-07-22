from google import genai
from app.core import settings
import logging

ai_client = None
logger = logging.getLogger(__name__)


def load_ai_client():
    global ai_client
    ai_client = genai.client.Client(api_key=settings.GEMINI_API_KEY)
    logger.info("AI client loaded successfully.")
    print("AI client loaded successfully.")


load_ai_client()
