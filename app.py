import streamlit as st
from PIL import Image, ImageDraw
import random
from io import BytesIO

# =========================
# CANVAS AYARLARI
# =========================
WIDTH, HEIGHT = 800, 600
BACKGROUND = (230, 240, 255)

# =========================
# PROMPT → PARAMETRE MOTORU
# =========================
def prompt_to_params(prompt: str):
    p = prompt.lower()

    # Varsayılan yaratık (bilinmeyen prompt)
    params = {
        "legs": 4,
        "body_ratio": 1.5,
        "spots": False,
        "tail": True,
        "color": (200, 200, 200)
    }

    if "inek" in p:
        params.update({
            "legs": 4,
            "body_ratio": 1.8,
            "spots": True,
            "tail": True,
            "color": (245, 245, 245)
        })

    if "kedi" in p:
        params.update({
            "legs": 4,
            "body_ratio": 1.2,
            "spots": False,
            "tail": True,
            "color": (210, 210, 210)
        })

    if "köpek" in p:
        params.update({
            "legs": 4,
            "body_ratio": 1.4,
            "spots": False,
            "tail": True,
            "color": (190, 190, 190)
        })

    if "balık" in p:
        params.update({
            "legs": 0,
            "body_ratio": 2.5,
            "spots": False,
            "tail": True,
            "color": (170, 210, 230)
        })

    if "ejderha" in p:
        params.update({
            "legs": 4,
            "body_ratio": 2.2,
            "spots": True,
            "tail": True,
            "color": (120, 180, 120)
        })

    return params

# =========================
# BENEK ÜRETİCİ
# =========================
def generate_spots(draw, x, y, w, h):
    for _ in range(8):
        sx = random.randint(x, x + w)
        sy = random.randint(y, y + h)
        r = random.randint(10, 25)
        draw.ellipse(
            [sx - r, sy - r, sx + r, sy + r],
            fill=(80, 80, 80)
        )

# =========================
# ANA ÜRETİM MOTORU
# =========================
def generate_creature(params, seed=None):
    if seed is None:
        seed = random.randint(0, 999999)
    random.seed(seed)

    img = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(img)

    # Gövde
    body_w = int(300 * params["body_ratio"])
    body_h = 160
    body_x = WIDTH // 2 - body_w // 2
    body_y = HEIGHT // 2 - body_h // 2

    draw.ellipse(
        [body_x, body_y, body_x + body_w, body_y + body_h],
        fill=params["color"],
        outline=(0, 0, 0),
        width=3
    )

    # Benek
    if params["spots"]:
        generate_spots(draw, body_x, body_y, body_w, body_h)

    # Bacaklar
    if params["legs"] > 0:
        spacing = body_w // (params["legs"] + 1)
        for i in range(params["legs"]):
            lx = body_x + spacing * (i + 1)
            ly = body_y + body_h
            draw.rectangle(
                [lx - 10, ly, lx + 10, ly + 80],
                fill=(100, 100, 100)
            )

    # Kuyruk
    if params["tail"]:
        tx = body_x + body_w
        ty = body_y + body_h // 2
        draw.line(
            [tx, ty, tx + 60, ty + 80],
            fill=(120, 120, 120),
            width=6
        )

    # Göz (basit ama karakter katar)
    eye_x = body_x + body_w // 4
    eye_y = body_y + body_h // 3
    draw.ellipse(
        [eye_x, eye_y, eye_x + 15, eye_y + 15],
        fill=(0, 0, 0)
    )

    return img, seed

# =========================
# STREAMLIT UI
# =========================
st.set_page_config(page_title="Prompt Creature Engine", layout="centered")
st.title("🧠 Prompt → Canlı Üretim Motoru")
st.write("Ne yazarsan ona göre **sıfırdan** bir şey üretilir. Foto yok. Kopya yok.")

prompt = st.text_input(
    "Ne çizelim?",
    placeholder="örnek: inek, kedi, balık, ejderha"
)

if st.button("ÜRET") and prompt.strip() != "":
    params = prompt_to_params(prompt)
    img, seed = generate_creature(params)

    buf = BytesIO()
    img.save(buf, format="PNG")

    st.image(
        buf.getvalue(),
        caption=f"Prompt: {prompt} | Seed: {seed}",
        use_container_width=True
    )

    st.code(params, language="python")
