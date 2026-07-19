from google import genai
from app.core import settings

ai_client = None

def load_ai_client():
    global ai_client
    ai_client = genai.client.Client(api_key=settings.GEMINI_API_KEY)
    print("AI client loaded successfully.")

load_ai_client()