import openai

openai.api_key = "TU_API_KEY_OPENAI"

def generate_recipe(ingredients: str, emotion: str):
    prompt = f"Genera una receta usando estos ingredientes: {ingredients}. Ajusta la receta a alguien que se siente {emotion}."

    # Nueva API de OpenAI
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente experto en recetas de cocina."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )

    # Extraer la respuesta
    recipe = response.choices[0].message.content.strip()
    return recipe
