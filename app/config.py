import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

DEEPSEEK_API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("DEEPSEEK_API_KEY")
