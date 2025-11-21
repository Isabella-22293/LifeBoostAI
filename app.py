import streamlit as st
from PIL import Image
from utils.emotion_utils import predict_emotion
from utils.food_utils import predict_food
from utils.llm_utils import generate_all_recommendations
import time
import json
import re
import random

# ================================
# Configuración general
# ================================
st.set_page_config(page_title="LifeBoost AI", layout="wide")

# ================================
# Cargar CSS
# ================================
def load_css(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("assets/style.css")

# ================================
# Playlist data
# (NO TOCADO)
# ================================
playlists = {
    "feliz": [
        "Happy - Pharrell Williams", "Can't Stop the Feeling - Justin Timberlake",
        "Uptown Funk - Mark Ronson ft. Bruno Mars", "Good as Hell - Lizzo",
        "Shake It Off - Taylor Swift", "I Gotta Feeling - Black Eyed Peas",
        "Walking on Sunshine - Katrina & The Waves", "Don't Stop Me Now - Queen",
        "Roar - Katy Perry", "Sugar - Maroon 5", "Best Day of My Life - American Authors",
        "Party in the U.S.A. - Miley Cyrus", "Cheerleader - OMI", "Raise Your Glass - P!nk",
        "Firework - Katy Perry", "Blinding Lights - The Weeknd", "Viva La Vida - Coldplay",
        "Shut Up and Dance - Walk The Moon", "Happy Now - Kygo ft. Sandro Cavazza",
        "Good Life - OneRepublic"
    ],
    "triste": [
        "Someone Like You - Adele", "Fix You - Coldplay", "Stay With Me - Sam Smith",
        "The Night We Met - Lord Huron", "Let Her Go - Passenger", "Hurt - Johnny Cash",
        "All I Want - Kodaline", "Skinny Love - Bon Iver", "Lost Boy - Ruth B",
        "Say You Love Me - Jessie Ware", "Unsteady - X Ambassadors",
        "I Will Always Love You - Whitney Houston", "Creep - Radiohead",
        "Everybody Hurts - R.E.M.", "Tears Dry on Their Own - Amy Winehouse",
        "Yesterday - The Beatles", "Nothing Compares 2 U - Sinead O'Connor",
        "Hallelujah - Jeff Buckley", "Jar of Hearts - Christina Perri",
        "When I Was Your Man - Bruno Mars"
    ],
    "enojado": [
        "Break Stuff - Limp Bizkit", "Killing in the Name - Rage Against The Machine",
        "You Oughta Know - Alanis Morissette", "Bodies - Drowning Pool", "Du Hast - Rammstein",
        "Smells Like Teen Spirit - Nirvana", "Given Up - Linkin Park", "Sabotage - Beastie Boys",
        "Dragula - Rob Zombie", "Eye of the Tiger - Survivor", "Psychosocial - Slipknot",
        "Fuel - Metallica", "Chop Suey - System Of A Down", "Pain - Three Days Grace",
        "Welcome to the Jungle - Guns N' Roses", "I Hate Everything About You - Three Days Grace",
        "Song 2 - Blur", "All the Small Things - Blink-182", "Thunderstruck - AC/DC",
        "Rollin' - Limp Bizkit"
    ],
    "neutral": [
        "Clocks - Coldplay", "Let It Be - The Beatles", "Viva La Vida - Coldplay",
        "Shape of You - Ed Sheeran", "Counting Stars - OneRepublic", "Yellow - Coldplay",
        "Imagine - John Lennon", "Something Just Like This - The Chainsmokers",
        "Hey Jude - The Beatles", "Photograph - Ed Sheeran", "Wonderwall - Oasis",
        "Chasing Cars - Snow Patrol", "Fix You - Coldplay", "No Surprises - Radiohead",
        "Hallelujah - Jeff Buckley", "Paradise - Coldplay", "The Scientist - Coldplay",
        "Let Her Go - Passenger", "Demons - Imagine Dragons", "All of Me - John Legend"
    ],
    "sorprendido": [
        "Surprise Yourself - Jack Garratt", "Adventure of a Lifetime - Coldplay",
        "On Top of the World - Imagine Dragons", "Wake Me Up - Avicii",
        "Good Time - Owl City & Carly Rae Jepsen", "Can't Hold Us - Macklemore",
        "Don't Stop Me Now - Queen", "Shake It Off - Taylor Swift",
        "Best Day Of My Life - American Authors", "Roar - Katy Perry",
        "Happy - Pharrell Williams", "Counting Stars - OneRepublic",
        "Uptown Funk - Mark Ronson ft. Bruno Mars", "Firework - Katy Perry",
        "Sugar - Maroon 5", "Viva La Vida - Coldplay", "Shut Up and Dance - Walk The Moon",
        "Blinding Lights - The Weeknd", "Good Life - OneRepublic", "Raise Your Glass - P!nk"
    ],
    "asco": [
        "Creep - Radiohead", "Hurt - Nine Inch Nails", "Somebody That I Used To Know - Gotye",
        "Boulevard of Broken Dreams - Green Day", "Everybody Hurts - R.E.M.",
        "Tears Dry On Their Own - Amy Winehouse", "Mad World - Gary Jules",
        "I Will Survive - Gloria Gaynor", "My Immortal - Evanescence", "Numb - Linkin Park",
        "Irreplaceable - Beyoncé", "Say Something - A Great Big World",
        "Jar of Hearts - Christina Perri", "Nothing Compares 2 U - Sinead O'Connor",
        "Lost Cause - Beck", "Blue Ain't Your Color - Keith Urban",
        "The A Team - Ed Sheeran", "Un-break My Heart - Toni Braxton",
        "Love the Way You Lie - Eminem ft. Rihanna", "Boulevard of Broken Dreams - Green Day"
    ],
    "miedo": [
        "Disturbia - Rihanna", "Thriller - Michael Jackson", "Somebody's Watching Me - Rockwell",
        "Fear of the Dark - Iron Maiden", "Monster - Lady Gaga", "Creep - Radiohead",
        "Zombie - The Cranberries", "Heathens - Twenty One Pilots",
        "Paint It Black - The Rolling Stones", "Enter Sandman - Metallica",
        "Sympathy for the Devil - Rolling Stones", "Black Hole Sun - Soundgarden",
        "Bury a Friend - Billie Eilish", "Don't Fear The Reaper - Blue Öyster Cult",
        "In The End - Linkin Park", "The Man Who Sold The World - Nirvana",
        "Bad Guy - Billie Eilish", "Highway to Hell - AC/DC",
        "Paranoid - Black Sabbath", "Thriller - Michael Jackson"
    ]
}

def generate_playlist(emotion, n_songs=20):
    emotion = emotion.lower()
    if emotion not in playlists:
        emotion = "neutral"
    songs = playlists[emotion]
    if len(songs) < n_songs:
        songs = songs * (n_songs // len(songs) + 1)
    return random.sample(songs, n_songs)

# ================================
# Idioma
# ================================
lang = st.sidebar.selectbox("Language / Idioma", ["Español", "English"])

if lang == "Español":
    t = {
        "welcome_title": "🌿 Bienvenido a LifeBoost AI",
        "welcome_sub": "Tu bienestar emocional guía tu fitness y tu cocina",
        "start": "Iniciar",
        "how_feel": "¿Cómo te sientes hoy?",
        "enter_emotion": "Escribe tu emoción",
        "upload_emotion_img": "O sube una imagen de tu rostro",
        "next": "Siguiente",
        "ingredients": "¿Qué ingredientes tenemos hoy?",
        "enter_ingredient": "Escribe tus ingredientes",
        "upload_food_img": "O sube una imagen de tus ingredientes",
        "generate": "Generar",
        "results": "Resultados personalizados",
        "mood_card": "Tu estado de ánimo es",
        "routine_card": "Rutina recomendada",
        "recipe_card": "Receta sugerida",
        "playlist_card": "Playlist sugerida",
        "home": "Inicio",
        "footer": "LifeBoost AI © 2025"
    }
    lang_code = "es"
    emotion_translations = {
        "happy": "feliz", "sad": "triste", "angry": "enojado", "neutral": "neutral",
        "surprised": "sorprendido", "disgust": "asco", "fear": "miedo"
    }
else:
    t = {
        "welcome_title": "🌿 Welcome to LifeBoost AI",
        "welcome_sub": "Your emotional well-being guides your fitness and cooking",
        "start": "Start",
        "how_feel": "How do you feel today?",
        "enter_emotion": "Type your emotion",
        "upload_emotion_img": "Or upload an image of your face",
        "next": "Next",
        "ingredients": "What ingredients do we have today?",
        "enter_ingredient": "Type your ingredients",
        "upload_food_img": "Or upload a photo of your ingredients",
        "generate": "Generate",
        "results": "Personalized Results",
        "mood_card": "Your mood is",
        "routine_card": "Recommended routine",
        "recipe_card": "Suggested recipe",
        "playlist_card": "Suggested playlist",
        "home": "Home",
        "footer": "LifeBoost AI © 2025"
    }
    lang_code = "en"
    emotion_translations = {}

# ================================
# Navegación
# ================================
if "page" not in st.session_state:
    st.session_state.page = "welcome"

def go_to(page):
    st.session_state.page = page

page = st.session_state.page

# ================================
# Funciones LLM (sin tocar)
# ================================
def extract_sections_fixed(text):
    receta_text, rutina_text, playlist_text = "", "", ""
    text = re.sub(r'\r\n', '\n', text).strip()

    receta_match = re.search(r"(Receta|Recipe)[\s\S]*?(Rutina|Routine|Ejercicio|Exercise)", text, re.IGNORECASE)
    if receta_match:
        receta_text = receta_match.group(0)
        receta_text = re.sub(r"(Rutina|Routine|Ejercicio|Exercise).*", "", receta_text, flags=re.IGNORECASE).strip()

    rutina_match = re.search(r"(Rutina|Routine|Ejercicio|Exercise)[\s\S]*?(Playlist|Música|Music|Canciones)", text, re.IGNORECASE)
    if rutina_match:
        rutina_text = rutina_match.group(0)
        rutina_text = re.sub(r"(Playlist|Música|Music|Canciones).*", "", rutina_text, flags=re.IGNORECASE).strip()

    playlist_match = re.search(r"(Playlist|Música|Music|Canciones)[\s\S]*", text, re.IGNORECASE)
    if playlist_match:
        playlist_text = playlist_match.group(0)

    return receta_text, rutina_text, playlist_text

def clean_output(text):
    if not text:
        return ""
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'[*_–-]+', '', text)
    text = text.replace('"', '').replace("'", '')
    text = "\n".join([line.strip() for line in text.splitlines()])
    text = re.sub(r'\n{2,}', '\n', text)
    return text.strip()

# ============================================================
# PÁGINAS
# ============================================================

# -------------------------
# WELCOME
# -------------------------
if page == "welcome":
    st.markdown("<div class='page-start'>", unsafe_allow_html=True)

    st.markdown(f"<h1 class='start-title'>{t['welcome_title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 class='start-sub'>{t['welcome_sub']}</h3>", unsafe_allow_html=True)

    if st.button(t["start"]):
        go_to("emotion")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# EMOTION
# -------------------------
elif page == "emotion":
    st.markdown("<div class='page-emotion'>", unsafe_allow_html=True)

    st.markdown(f"<h2 class='page-heading'>{t['how_feel']}</h2>", unsafe_allow_html=True)

    emotion_text = st.text_input(t["enter_emotion"])
    emotion_img = st.file_uploader(t["upload_emotion_img"], type=["jpg", "jpeg", "png"])
    emotion_detected = None

    if emotion_img:
        image = Image.open(emotion_img)
        st.image(image, use_container_width=True)
        emotion_detected = predict_emotion(image)
    elif emotion_text:
        emotion_detected = emotion_text.lower()

    if (emotion_text or emotion_img) and st.button(t["next"]):
        st.session_state.emotion = emotion_detected
        go_to("ingredients")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# INGREDIENTS
# -------------------------
elif page == "ingredients":
    st.markdown("<div class='page-ingredients'>", unsafe_allow_html=True)

    st.markdown(f"<h2 class='page-heading'>{t['ingredients']}</h2>", unsafe_allow_html=True)

    ingredient_text = st.text_input(t["enter_ingredient"])
    ingredient_img = st.file_uploader(t["upload_food_img"], type=["jpg", "jpeg", "png"])
    main_ingredient = None

    if ingredient_img:
        food_image = Image.open(ingredient_img)
        st.image(food_image, use_container_width=True)
        main_ingredient = predict_food(food_image)
    elif ingredient_text:
        main_ingredient = ingredient_text.lower()

    if (ingredient_text or ingredient_img) and st.button(t["generate"]):
        st.session_state.ingredient = main_ingredient
        go_to("results")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# RESULTS
# -------------------------
elif page == "results":
    st.markdown("<div class='page-results'>", unsafe_allow_html=True)

    st.markdown(f"<h2 class='page-heading'>{t['results']}</h2>", unsafe_allow_html=True)

    emotion = st.session_state.get("emotion", "neutral")
    ingredient = st.session_state.get("ingredient", "none")
    emotion_display = emotion_translations.get(emotion.lower(), emotion.capitalize()) if lang_code == "es" else emotion.capitalize()

    with st.spinner("Generando recomendaciones..." if lang_code == "es" else "Generating recommendations..."):
        response = generate_all_recommendations(emotion, ingredient, lang_code)
        time.sleep(2)

    response_text = json.dumps(response, ensure_ascii=False) if isinstance(response, dict) else str(response)
    receta_text, rutina_text, playlist_text = extract_sections_fixed(response_text)

    receta_text = clean_output(receta_text)
    rutina_text = clean_output(rutina_text)
    playlist_text = clean_output(playlist_text)

    st.markdown(f"### {t['mood_card']}")
    st.write(emotion_display)

    st.markdown(f"### {t['recipe_card']}")
    st.text_area("", receta_text, height=250, disabled=True)

    st.markdown(f"### {t['routine_card']}")
    st.text_area("", rutina_text, height=250, disabled=True)

    st.markdown(f"### {t['playlist_card']}")
    playlist_songs = generate_playlist(emotion_display, 20)
    for i, song in enumerate(playlist_songs, 1):
        st.write(f"{i}. {song}")

    if st.button(t["home"], key="home_btn"):
        go_to("welcome")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# FOOTER
# -------------------------
st.markdown(f"<p class='footer'>{t['footer']}</p>", unsafe_allow_html=True)

