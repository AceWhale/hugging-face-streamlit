import os
import urllib.parse
import requests
import streamlit as st
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

def get_secret(name):
    if name in st.secrets:
        return st.secrets[name]
    return os.getenv(name)

HF_API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
HF_TOKEN = get_secret("HF_TOKEN")

def generate_image(prompt):
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed=42"

        response = requests.get(url, timeout=45)

        if response.status_code == 200:
            return response.content, None
        else:
            return None, f"Сервіс тимчасово непрацює ({response.status_code})"
    except requests.exceptions.Timeout:
        return None, "Time-out"
    except Exception as e:
        return None, f"Помилка підключення: {e}"

st.title("AI Creative Studio")
st.write("Напиши яке зображення хочеш отримати - ШІ створить його безкоштовно")

prompt = st.text_area("Опис зображення (промпт)", placeholder="Наприклад: логотип кафе у формі зерна")

STYLES = {
    "Без стилю (як написано)": "",
    "Реалістичне фото": ", photorealistic, high detail, natural lighting",
    "Акварель": ", watercolor painting style, soft edges, pastel colors",
    "Мультфільм": ", 3D animated movie style, vibrant colors, friendly look",
    "Піксель-арт": ", pixel art style, 16-bit retro game aesthetic",
}

style_choice = st.selectbox("Вибери стиль зображення:", list(STYLES.keys()))

if st.button("Сгенерувати зображення") and prompt:
    final_prompt = prompt + STYLES[style_choice]

    with st.spinner("AI створює зображення"):
        image_bytes, error = generate_image(final_prompt)

    if error:
        st.error(f"Не вдалося сгенерувати зображення: {error}")
    elif image_bytes:
        st.image(image_bytes, caption=f"Стиль: {style_choice}", use_container_width=True)
        st.session_state["last_image"] = image_bytes

if "last_image" in st.session_state:
    st.download_button(
        label="Завантажити фото",
        data=st.session_state["last_image"],
        file_name="ai_studio_result.png",
        mime="image/png"
    ) 