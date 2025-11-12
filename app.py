import streamlit as st
from PIL import Image
from utils.emotion_utils import predict_emotion
from utils.food_utils import predict_food
from utils.llm_utils import generate_recipe

# Import CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Titles
st.markdown("<h1 style='text-align: center;'>LifeBoost AI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Tu bienestar emocional guía tu fitness y tu cocina </h3>", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Opciones")
st.sidebar.info("Sube tu selfie y foto de ingredientes para obtener recomendaciones personalizadas.")

# Step 1 - Selfie
st.subheader("Sube tu selfie")
selfie_file = st.file_uploader("Selecciona una imagen de tu rostro", type=['jpg', 'png', 'jpeg'])

emotion = None
if selfie_file:
    image = Image.open(selfie_file)
    st.image(image, caption="Tu selfie", use_container_width=True)

    emotion = predict_emotion(image)
    st.markdown(f"<div class='card-{emotion}'>Estado emocional detectado: <b>{emotion}</b></div>", unsafe_allow_html=True)

# Step 2 - Ingredients
st.subheader("Sube una foto de tus ingredientes")
food_file = st.file_uploader("Selecciona la foto de tus ingredientes", type=['jpg', 'png', 'jpeg'])

if food_file and emotion:
    food_image = Image.open(food_file)
    st.image(food_image, caption="Ingredientes", use_container_width=True)

    main_ingredient = predict_food(food_image)
    st.markdown(f"<div class='card-neutral'>Ingrediente principal detectado: <b>{main_ingredient}</b></div>", unsafe_allow_html=True)

    # Generate recipe
    recipe = generate_recipe(main_ingredient, emotion)
    st.markdown(f"<div class='card-{emotion}'><h4>🍽️ Receta sugerida</h4>{recipe}</div>", unsafe_allow_html=True)

    # Fitness routine
    routines = {
        'happy': 'Cardio ligero y estiramiento • 15 min',
        'sad': 'Yoga y meditación • 20 min',
        'angry': 'Boxeo o golpe al saco • 20 min',
        'neutral': 'Caminata ligera • 20 min',
        'surprised': 'Entrenamiento HIIT • 15 min'
    }
    st.markdown(f"<div class='card-{emotion}'><h4>🏋️ Rutina recomendada</h4>{routines.get(emotion)}</div>", unsafe_allow_html=True)

    # Playlist
    playlists = {
        'happy': 'https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC',
        'sad': 'https://open.spotify.com/playlist/37i9dQZF1DX7qK8ma5wgG1',
        'angry': 'https://open.spotify.com/playlist/37i9dQZF1DX1g0iEXLFycr',
        'neutral': 'https://open.spotify.com/playlist/37i9dQZF1DWZqUHC2tviPw',
        'surprised': 'https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0'
    }
    st.markdown(f"<div class='card-{emotion}'><h4>🎵 Playlist sugerida</h4><a href='{playlists.get(emotion)}' target='_blank'>Escuchar en Spotify</a></div>", unsafe_allow_html=True)
