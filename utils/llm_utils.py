import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargar la API Key desde .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Inicializar cliente para usar OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)