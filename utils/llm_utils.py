import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError("No se encontró la variable OPENROUTER_API_KEY en el archivo .env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)

# ===========================================
# Generar recomendaciones con formato estándar
# ===========================================
def generate_all_recommendations(emotion: str, ingredient: str, lang: str = "es"):
    """
    Usa el LLM para generar una receta, rutina y playlist personalizada.
    Devuelve texto en formato delimitado por etiquetas fijas.
    """

    if lang == "en":
        prompt = f"""
You are a wellness coach and culinary expert.

The user feels **{emotion}** and has **{ingredient}** available.

Please generate the response **in this exact structured format**:

Receta:
(Write the full recipe with ingredients, quantities, steps, and emotional benefits.)

Rutina:
(Describe a physical routine with warm-up, main part, and stretching related to the emotion.)

Playlist:
(Give a playlist name, short description, and 5 suggested songs to improve the user's mood.)
"""
        system_message = "You are a compassionate AI wellness assistant."
    else:
        prompt = f"""
Eres un coach de bienestar y experto en cocina saludable.

El usuario se siente **{emotion}** y tiene **{ingredient}** como ingrediente principal.

Por favor responde **exactamente con el siguiente formato**:

Receta:
(Escribe la receta completa con ingredientes, cantidades, pasos y beneficios emocionales.)

Rutina:
(Describe una rutina física con calentamiento, parte principal y estiramiento, que ayude con el estado de ánimo.)

Playlist:
(Da un nombre, descripción y 5 canciones sugeridas que mejoren el ánimo del usuario.)
"""
        system_message = "Eres un asistente empático especializado en bienestar emocional, cocina saludable y actividad física."

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3.1-70b-instruct",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=900,
        )

        text = response.choices[0].message.content.strip()

        # Devolver texto completo (el app.py lo separa con extract_section)
        return text

    except Exception as e:
        print(f"[Error LLM]: {e}")
        return """
Receta:
No se pudo generar la receta.

Rutina:
No se pudo generar la rutina.

Playlist:
No se pudo generar la playlist.
"""
