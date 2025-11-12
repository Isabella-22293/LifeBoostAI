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

def generate_all_recommendations(ingredient: str, emotion: str):
    """
    Usa el LLM para generar receta, rutina y playlist emocional en formato JSON.
    """

    prompt = f"""
    Eres un asistente experto en bienestar emocional, fitness y cocina saludable.
    El usuario se siente '{emotion}' y tiene '{ingredient}' como ingrediente principal.

    Devuelve tu respuesta en formato JSON con las siguientes claves:
    - receta: texto con una receta completa y saludable.
    - rutina: rutina física ideal según el estado emocional.
    - playlist: breve descripción o lista musical sugerida.

    Ejemplo:
    {{
      "receta": "Ensalada energizante de aguacate y garbanzos...",
      "rutina": "Yoga suave de 15 minutos para mejorar el ánimo...",
      "playlist": "Playlist relajante de sonidos naturales y pop suave..."
    }}
    """
