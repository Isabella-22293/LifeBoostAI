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
