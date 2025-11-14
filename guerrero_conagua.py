import streamlit as st

import requests
from io import BytesIO
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")

    # --- Configuración ---
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}",    "User-Agent": "my-app"}
API_URL = "https://api.github.com/repos/thewhediaz/SAT/contents/media/CURRENT_2H_colores_windy"

    # --- Obtener lista de archivos en GitHub ---
response = requests.get(API_URL, headers=HEADERS)
files = response.json()

if isinstance(files, dict) and files.get("message"):
    st.stop()  # Error de API → no mostrar nada

    # Buscar GIF, MP4 y PNGs
gif_file = next((f for f in files if f["name"] == "animacion.gif"), None)
mp4_file = next((f for f in files if f["name"] == "animacion.mp4"), None)

png_files = sorted(
    [f for f in files if f["name"].endswith(".png")],
    key=lambda x: x["name"]  # nombres ya ordenados
)

    # Si no hay GIF o no hay última imagen → no mostrar nada
if not gif_file or not mp4_file or not png_files:
    st.stop()

    # --- Mostrar GIF animado ---
st.image(gif_file["download_url"], width='stretch')

    # --- Botón descargar MP4 ---
mp4_bytes = requests.get(mp4_file["download_url"]).content
st.download_button(
    label="Descargar animación MP4",
    data=mp4_bytes,
    file_name="animacion.mp4",
    mime="video/mp4"
)

    # --- Botón descargar última imagen PNG ---
last_png_url = png_files[-1]["download_url"]
last_png_bytes = requests.get(last_png_url).content

st.download_button(
    label="Descargar última imagen",
    data=last_png_bytes,
    file_name="ultima_imagen.png",
    mime="image/png"
)

# --- AUTOREFRESH EN MINUTOS ESPECÍFICOS ---
target_minutes = [2, 7, 12, 17, 22, 27, 32, 37, 42, 47, 52, 57]

now = datetime.now()
minute = now.minute
second = now.second

    # Buscar el próximo minuto objetivo
for m in target_minutes:
    if m > minute or (m == minute and second == 0):
        next_target = m
        break
else:
    next_target = target_minutes[0]

    # Segundos hasta el refresh
delta_seconds = (next_target - minute) * 60 - second
if delta_seconds < 0:
    delta_seconds += 3600

st_autorefresh(interval=delta_seconds * 1000, key="autorefresh")
