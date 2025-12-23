import streamlit as st
import requests
import time

# =========================
# API URL'LERİ (YENİ ROUTER)
# =========================
SD_API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-2-1"
st.write("TOKEN OK:", st.secrets["HF_API_KEY"][:6])

TR_EN_API_URL = "https://router.huggingface.co/hf-inference/models/Helsinki-NLP/opus-mt-tr-en"

HEADERS = {
    "Authorization": f"Bearer {st.secrets['HF_API_KEY']}"
}

# =========================
# 1️⃣ TÜRKÇE → İNGİLİZCE
# =========================
def translate_tr_to_en(text):
    payload = {"inputs": text}

    for _ in range(3):
        response = requests.post(
            TR_EN_API_URL,
            headers=HEADERS,
            json=payload
        )

        if response.status_code == 503:
            time.sleep(3)
            continue

        if response.status_code == 200:
            result = response.json()
            return result[0]["translation_text"]

    return text  # fallback

# =========================
# 2️⃣ PROMPT MOTORU
# =========================
def syntho_prompt(user_prompt_tr):
    prompt_en = translate_tr_to_en(user_prompt_tr)

    base_prompt = (
        "ultra realistic photo, high detail, sharp focus, "
        "natural lighting, realistic textures"
    )

    final_prompt = f"{base_prompt}, {prompt_en}"
    return final_prompt, prompt_en

# =========================
# 3️⃣ GÖRSEL ÜRETİM
# =========================
def generate_image(prompt):
    payload = {
    "inputs": prompt,
    "options": {
        "wait_for_model": True
    }
}

    for _ in range(5):
        response = requests.post(
            SD_API_URL,
            headers=HEADERS,
            json=payload
        )

        if response.status_code in (503, 504):
            time.sleep(5)
            continue

        if response.status_code == 429:
            time.sleep(10)
            continue

        if response.status_code == 200:
            return response.content

    st.error("Servis şu an yoğun, tekrar dene.")
    st.stop()

# =========================
# 4️⃣ STREAMLIT UI
# =========================
st.set_page_config(page_title="Syntho AI", layout="centered")
st.title("🧬 Syntho AI")
st.caption("Resim Üretme Aracı!")

user_prompt = st.text_input(
    "Ne üretelim?",
    placeholder="örnek: gerçekçi balık, sisli dağ, sinematik portre"
)

if st.button("ÜRET") and user_prompt.strip():
    with st.spinner("Syntho AI üretiyor..."):
        final_prompt, translated = syntho_prompt(user_prompt)
        img = generate_image(final_prompt)

        st.image(img, caption="Syntho AI çıktısı")
        st.subheader("🔎 Kullanılan İngilizce Prompt")
        st.code(final_prompt)
