import streamlit as st
import requests

# =========================
# API AYARLARI
# =========================
SD_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
TR_EN_API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-tr-en"

HEADERS = {
    "Authorization": f"Bearer {st.secrets['HF_API_KEY']}"
}

# =========================
# TÜRKÇE → İNGİLİZCE ÇEVİRİ
# =========================
import time
import time

def generate_image(prompt):
    payload = {"inputs": prompt}

    for attempt in range(5):
        response = requests.post(SD_API_URL, headers=HEADERS, json=payload)

        # Model yükleniyorsa veya yoğunluk varsa bekle
        if response.status_code in (503, 504):
            time.sleep(5)
            continue

        # Rate limit (free quota dolu)
        if response.status_code == 429:
            time.sleep(10)
            continue

        # Başarılı
        if response.status_code == 200:
            return response.content

    # Hepsi başarısızsa kullanıcıya düzgün hata ver
    st.error("🚫 Şu an görsel üretim servisi yoğun. Lütfen biraz sonra tekrar dene.")
    st.stop()



# =========================
# PROMPT MOTORU (Syntho AI ZEKA)
# =========================
def syntho_prompt(user_prompt_tr):
    prompt_en = translate_tr_to_en(user_prompt_tr)

    base = "ultra realistic photo, high detail, sharp focus, natural lighting"

    final_prompt = f"{base}, {prompt_en}"
    return final_prompt, prompt_en

# =========================
# GÖRSEL ÜRETİM
# =========================
def generate_image(prompt):
    payload = {"inputs": prompt}
    response = requests.post(SD_API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.content

# =========================
# STREAMLIT UI
# =========================
st.set_page_config(page_title="Syntho AI", layout="centered")
st.title("🧬 Syntho AI — Realistic Image Engine")
st.caption("Gerçekçiliğin ötesi!")

user_prompt = st.text_input(
    "Ne üretelim? (Türkçe yazabilirsin)",
    placeholder="örnek: gerçekçi balık, sisli dağ, kedi portresi"
)

if st.button("ÜRET") and user_prompt.strip():
    with st.spinner("Syntho AI düşünüyor..."):
        final_prompt, translated = syntho_prompt(user_prompt)
        img_bytes = generate_image(final_prompt)

        st.image(img_bytes, caption="Üretilen Görsel")
        st.subheader("🔎 Kullanılan İngilizce Prompt")
        st.code(final_prompt, language="text")
