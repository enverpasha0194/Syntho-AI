import streamlit as st
import requests
import time
import base64
from PIL import Image
import io

# =========================
# AYARLAR
# =========================
SD_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
TR_EN_API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-tr-en"

HF_TOKEN = st.secrets["HF_API_KEY"]

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# =========================
# 1️⃣ TÜRKÇE → İNGİLİZCE
# =========================
def translate_tr_to_en(text):
    payload = {"inputs": text}

    r = requests.post(TR_EN_API_URL, headers=HEADERS, json=payload)

    if r.status_code != 200:
        st.warning("Çeviri servisi patladı, Türkçe prompt devam ediliyor.")
        return text

    data = r.json()
    return data[0]["translation_text"]

# =========================
# 2️⃣ PROMPT MOTORU
# =========================
def syntho_prompt(user_prompt_tr):
    prompt_en = translate_tr_to_en(user_prompt_tr)

    base_prompt = (
        "ultra realistic photo, high detail, sharp focus, "
        "cinematic lighting, realistic textures, 8k"
    )

    final_prompt = f"{base_prompt}, {prompt_en}"
    return final_prompt, prompt_en

# =========================
# 3️⃣ GÖRSEL ÜRETİM
# =========================
def generate_image(prompt):
    payload = {
        "inputs": prompt
    }

    r = requests.post(SD_API_URL, headers=HEADERS, json=payload)

    if r.status_code != 200:
        st.error("Stable Diffusion hata verdi:")
        st.code(r.text)
        st.stop()

    # HF image → bytes
    image = Image.open(io.BytesIO(r.content))
    return image

# =========================
# 4️⃣ STREAMLIT UI
# =========================
st.set_page_config(page_title="Syntho AI", layout="centered")

st.title("🧬 Syntho AI")
st.caption("Türkçe yaz → İngilizce düşün → Gerçekçi görsel üret")

user_prompt = st.text_input(
    "Ne üretelim?",
    placeholder="örnek: sinematik asker portresi, sisli dağ, cyberpunk şehir"
)

if st.button("ÜRET") and user_prompt.strip():
    with st.spinner("Syntho AI düşünüyor..."):
        final_prompt, translated = syntho_prompt(user_prompt)
        img = generate_image(final_prompt)

        st.image(img, caption="Syntho AI çıktısı")
        st.subheader("🔎 Kullanılan İngilizce Prompt")
        st.code(final_prompt)
