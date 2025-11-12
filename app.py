import streamlit as st
from PIL import Image
import json
from utils.emotion_utils import predict_emotion
from utils.food_utils import predict_food
from utils.llm_utils import generate_all_recommendations  # función extendida

# ==============================
# 🖌️ Cargar estilos CSS
# ==============================
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==============================
# 🧠 Títulos e información
# ==============================
st.markdown("<h1 style='text-align: center;'>🌿 LifeBoost AI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Tu bienestar emocional guía tu fitness y tu cocina 🍽️</h3>", unsafe_allow_html=True)

st.sidebar.title("Opciones")
st.sidebar.info("Sube tu selfie y una foto de tus ingredientes para obtener recomendaciones personalizadas de bienestar, recetas y música.")

# ==============================
# 🧍 Paso 1 - Análisis emocional
# ==============================
st.subheader("🧠 Sube tu selfie")
selfie_file = st.file_uploader("Selecciona una imagen de tu rostro", type=['jpg', 'png', 'jpeg'])

emotion = None
if selfie_file:
    image = Image.open(selfie_file)
    st.image(image, caption="Tu selfie", use_container_width=True)

    # Detectar emoción
    emotion = predict_emotion(image)
    st.markdown(f"<div class='card-{emotion}'>Estado emocional detectado: <b>{emotion}</b></div>", unsafe_allow_html=True)

# ==============================
# 🥦 Paso 2 - Ingredientes
# ==============================
st.subheader("🍅 Sube una foto de tus ingredientes")
food_file = st.file_uploader("Selecciona la foto de tus ingredientes", type=['jpg', 'png', 'jpeg'])

if food_file and emotion:
    food_image = Image.open(food_file)
    st.image(food_image, caption="Ingredientes detectados", use_container_width=True)

    # Detectar alimento principal
    main_ingredient = predict_food(food_image)
    st.markdown(f"<div class='card-neutral'>Ingrediente principal detectado: <b>{main_ingredient}</b></div>", unsafe_allow_html=True)

    # ==============================
    # 🧘‍♀️ Paso 3 - Generar todo con LLM
    # ==============================
    st.markdown("<h3>🌿 Generando recomendaciones personalizadas...</h3>", unsafe_allow_html=True)

    # Llamar al modelo de lenguaje
    response_text = generate_all_recommendations(main_ingredient, emotion)

    try:
        data = json.loads(response_text)

        st.markdown(f"<div class='card-{emotion}'><h4>🍽️ Receta sugerida</h4>{data['receta']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card-{emotion}'><h4>🏋️ Rutina recomendada</h4>{data['rutina']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='card-{emotion}'><h4>🎵 Playlist sugerida</h4>{data['playlist']}</div>", unsafe_allow_html=True)

    except Exception:
        st.error("⚠️ No se pudo interpretar la respuesta del modelo. Aquí está la respuesta bruta:")
        st.text(response_text)

# ==============================
# 🧩 Mensaje final
# ==============================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>💚 Desarrollado con IA — LifeBoost AI © 2025</p>", unsafe_allow_html=True)
